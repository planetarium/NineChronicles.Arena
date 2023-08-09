import os
import random
from typing import List, Optional

from common import logger
from common.const import HOST_DICT
from common.models.block import Block
from common.schemas.block import BlockSchema
from common.utils.aws import fetch_secrets
from common.utils.gql import execute_gql
from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import sessionmaker, scoped_session

from arena_updater import apply_arena_actions
from table_patch import apply_patch_table

MAX_BLOCKS_PER_REQUEST = 10

DB_URI = os.environ.get("DB_URI")
if os.environ.get("SECRET_ARN"):
    db_password = fetch_secrets(os.environ.get("REGION_NAME"), os.environ.get("SECRET_ARN"))["password"]
    DB_URI = DB_URI.replace("[DB_PASSWORD]", db_password)

engine = create_engine(DB_URI, pool_size=5, max_overflow=5)


def fetch_block(host: str, block_index: Optional[int], block_hash: Optional[int]):
    url = f"{host}/graphql/explorer"
    if not (block_index or block_hash):
        raise ValueError("Either block_index or block_hash must be provided")
    query_1 = """{
    blockQuery {
        block (
    """
    query_2 = """
    )
    } {
        index
        hash
        timestamp
        transactions {
            actions { json }
        }
    }
    }
    """
    if block_index:
        query = query_1 + f"index: {block_index}" + query_2
    else:
        query = query_1 + f"hash: \"{block_hash}\"" + query_2

    data = execute_gql(url, query)
    return BlockSchema(**data["blockQuery"]["block"])


def fetch_blocks(host: str, start: int = None, limit: int = None) -> List[BlockSchema]:
    url = f"{host}/graphql/explorer"
    desc = "false"
    if not start:
        desc = "true"

    if limit:
        limit = min(limit, MAX_BLOCKS_PER_REQUEST)  # Max 100 blocks

    query_1 = "{blockQuery { blocks ("
    query_2 = ") {index hash timestamp transactions {actions {json}}}}}"
    query = f"{query_1} desc: {desc} limit: {limit}"
    if start is not None:
        query += f" offset: {start + 1}"
    query += query_2
    data = execute_gql(url, query)
    return sorted([BlockSchema(**x) for x in data["blockQuery"]["blocks"]], key=lambda x: x.index)


def update_block(sess, block_data: List[BlockSchema]):
    for block in block_data:
        sess.add(Block(index=block.index, hash=block.hash, timestamp=block.timestamp))
    sess.commit()
    logger.info(f"{len(block_data)} blocks are updated. The last block index is: {max([x.index for x in block_data])}")


def handle(event, context):
    stage = os.environ.get("STAGE", "development")
    sess = None
    try:
        sess = scoped_session(sessionmaker(bind=engine))
        last_block_index = sess.scalar(select(Block.index).order_by(desc(Block.index)))
        block_data = fetch_blocks(random.choice(HOST_DICT[stage]), start=last_block_index, limit=10)
        # DISCUSS: Should these 3 functions be atomic DB transaction?
        apply_arena_actions(sess, block_data)
        apply_patch_table(sess, block_data)
        update_block(sess, block_data)
        sess.commit()
    finally:
        if sess is not None:
            sess.close()


if __name__ == "__main__":
    handle(None, None)
