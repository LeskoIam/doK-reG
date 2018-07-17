from app import db

__author__ = 'mpolensek'
# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.


def execute_query(query: str, as_list=False):
    """Execute raw sql query

    :param query: raw sql query
    :param as_list:  return result as list
    :return: result as object
    """
    result = db.engine.execute(query)
    if as_list:
        result = list(result)
    return result


if __name__ == '__main__':
    from app.common.db_queries import Queries
    queries = Queries()
    sql_str = queries.document_history(document_id=5)

    res = execute_query(sql_str)
    print(res)
    print(dir(res))
    print()

    for row in res:
        print(row)
        # print(dir(row))
        # print(row.keys())
        print(row.revision)
