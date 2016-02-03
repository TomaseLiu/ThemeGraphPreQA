import db_tools


cursor,conn = db_tools.conn()
get_all_anno_data_sql = "SELECT TASK_NAME1 AS ThemeName, TASK_NAME2 as NewsID, PAGE_ID as NewsPageID, USER_NAME as UserName, CHOICE as AnnoCorr, REMARK1 as AnnoAdd, REMARK2 as AnnoDel, INSERT_TIME as InsertTime FROM theme_context_mark_task"
insert_anno_rcd_into_new_table = "INSERT INTO theme_news_anno (ThemeName, ThemeVersionID, NewsID, NewsPageID, UserName, AnnoCorr, AnnoAdd, AnnoDel) VALUES ('%s', '0.1', '%s', %d, '%s', '%s', '%s', '%s')"
cursor = db_tools.query(cursor, get_all_anno_data_sql)


cursor_insert, conn_insert = db_tools.conn()
row = db_tools.fetch_one_row(cursor)
while row != None:
    ThemeName = row['ThemeName']
    NewsID = row['NewsID']
    NewsPageID = int(row['NewsPageID'])
    UserName = row['UserName']
    AnnoCorr = row['AnnoCorr']
    AnnoAdd = row['AnnoAdd']
    AnnoDel = row['AnnoDel']
    InsertTime = row['InsertTime']

    db_tools.insert(cursor_insert, conn_insert, insert_anno_rcd_into_new_table % (ThemeName, NewsID, NewsPageID, UserName, AnnoCorr, AnnoAdd, AnnoDel))

    row = db_tools.fetch_one_row(cursor)

db_tools.close(cursor_insert)
db_tools.close(cursor)
