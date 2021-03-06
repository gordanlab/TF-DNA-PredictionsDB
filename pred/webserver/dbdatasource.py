import psycopg2.extras

from pred.queries.datasourcesquery import DataSourcesQuery, DataSourcesQueryNames


class DataSources(object):
    def __init__(self, db):
        self.db = db

    def get_items(self):
        query, params = DataSourcesQuery().make_query_and_params()
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, params)
        items = []
        for row in cur.fetchall():
            downloaded = row[DataSourcesQueryNames.DOWNLOADED];
            downloaded_str = downloaded.strftime("%m/%d/%Y %H:%M")
            items.append({
                DataSourcesQueryNames.DESCRIPTION: row[DataSourcesQueryNames.DESCRIPTION],
                DataSourcesQueryNames.DOWNLOADED: downloaded_str,
                DataSourcesQueryNames.URL: row[DataSourcesQueryNames.URL],
                'dataSourceType': row[DataSourcesQueryNames.DATA_SOURCE_TYPE]
            })
        cur.close()
        return items
