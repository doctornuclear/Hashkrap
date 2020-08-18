from hashkrap import get_db

def get_hashtags_from_db(search, engagement, sort_by):
    print(search, engagement, sort_by)
    order_by_query = get_sort_by_query(sort_by, search, engagement)
    query = '''
            SELECT hashtag,post_count,
                CASE 
                    WHEN {1}/AVG_LIKES <=0.3 THEN 'Very Low'                    
                    WHEN {1}/AVG_LIKES <=0.6 THEN 'Low'                  
                    WHEN {1}/AVG_LIKES <=1 THEN 'Medium'                    
                    WHEN {1}/AVG_LIKES <=1.5 THEN 'High'                  
                ELSE
                    'Very High'                                                
                END PROBABILITY,

                CASE
                    WHEN {1}/AVG_LIKES >= 1  THEN 'Ranking'
                ELSE 
                    'Exposure'
                END PURPOSE
            ,max_likes,min_likes,avg_likes,max_comments,min_comments,avg_comments
            FROM hashtag_details
            WHERE hashtag LIKE '%{2}%'
            {0}
            '''.format(order_by_query, engagement, search)
    # print(query)
    cursor = get_db().cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


def get_sort_by_query(sort_by, keyword, engagement):
    sort_by_top = '''
                ORDER BY 
                CASE
                    WHEN hashtag LIKE '#{0}' THEN 1
                    WHEN hashtag LIKE '#{0}%' THEN 2
                    WHEN hashtag LIKE '%{0}' THEN 3
                    ELSE 4
                END
                '''.format(keyword)
    sort_by_me = '''
                ORDER BY
                CASE 
                    WHEN {0}/AVG_LIKES <=0.3 THEN 5                    
                    WHEN {0}/AVG_LIKES <=0.6 THEN 4                  
                    WHEN {0}/AVG_LIKES <=1 THEN 3                  
                    WHEN {0}/AVG_LIKES <=1.5 THEN 1                  
                ELSE
                    2                                                
                END
                '''.format(engagement)
    if sort_by == "me":
        return sort_by_me
    return sort_by_top


def get_table_hashtags(hashtags_list, offset=0, per_page=50):
    return hashtags_list[offset: offset + per_page]


def not_found(keyword, avg_likes, username):
    print("SERVER: saving new Not_found hashtag")
    query = '''
            INSERT INTO not_found
            ('keyword', 'username', 'avg_likes', 'completed', 'added_to_db')
            VALUES (?,?,?,0,0)
            '''
    values = (keyword, username, avg_likes)
    try:
        cursor = get_db().cursor()
        cursor.execute(query, values)
        get_db().commit()
        return True
    except:
        return False

