from dotenv import load_dotenv
import os
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()


def db_user_fetcher(user_id, data_type):
    try:
        connect = psycopg2.connect(
            user=os.getenv('PG_USER'),
            password=os.getenv('PG_PASSWORD'),
            host=os.getenv('PG_HOST'),
            port=os.getenv('PG_PORT'),
            database=os.getenv('PG_DATABASE')
        )
        if data_type == 'USER_ETAB':
            idx = 0
        if data_type == 'CONTENT_ETAB':
            idx = 1
        if data_type == 'USER_SERVICE':
            idx = 2
        if data_type == 'CONTENT_SERVICE':
            idx = 3
        if data_type == 'CONTENT_RYTHME':
            idx = 4

        sql_queries = [
            {'USER_ETAB': """
         WITH
            missions_select AS (
                SELECT
                u.id AS user_id,
                uet.created_at,
                CASE WHEN uet.establishment_type = 'clinic' THEN 1 ELSE 0 END AS clinic,
                CASE WHEN uet.establishment_type = 'ehpad_rh' THEN 1 ELSE 0 END AS ehpad_rh,
                CASE WHEN uet.establishment_type = 'had' THEN 1 ELSE 0 END AS had,
                CASE WHEN uet.establishment_type = 'hea_cen' THEN 1 ELSE 0 END AS hea_cen,
                CASE WHEN uet.establishment_type = 'hea_hou' THEN 1 ELSE 0 END AS hea_hou,
                CASE WHEN uet.establishment_type = 'home_consult'  THEN 1 ELSE 0 END AS home_consult,
                CASE WHEN uet.establishment_type = 'hospi' THEN 1 ELSE 0 END AS hospi,
                CASE WHEN uet.establishment_type = 'labo' THEN 1 ELSE 0 END AS labo,
                CASE WHEN uet.establishment_type = 'lib_off' THEN 1 ELSE 0 END AS lib_off,
                CASE WHEN uet.establishment_type = 'other_ms' THEN 1 ELSE 0 END AS other_ms,
                CASE WHEN uet.establishment_type = 'priv_comp'  THEN 1 ELSE 0 END AS priv_comp,
                CASE WHEN uet.establishment_type = 'ssr'  THEN 1 ELSE 0 END AS ssr,
                CASE WHEN uet.establishment_type = 'teleconsult'  THEN 1 ELSE 0 END AS teleconsult
                FROM
                medelse.user_establishment_type uet
                JOIN medelse.user u ON u.id = uet.user_id
                WHERE uet.deleted_at is null
            )
            SELECT
                ms.user_id,
                SUM(ms.clinic) AS clinic,
                SUM(ms.ehpad_rh) AS ehpad_rh,
                SUM(ms.had) AS had,
                SUM(ms.hea_cen) AS hea_cen,
                SUM(ms.hea_hou) AS hea_hou,
                SUM(ms.home_consult) AS home_consult,
                SUM(ms.hospi) AS hospi,
                SUM(ms.labo) AS labo,
                SUM(ms.lib_off) AS lib_off,
                SUM(ms.other_ms) AS other_ms,
                SUM(ms.priv_comp) AS priv_comp,
                SUM(ms.ssr) AS ssr,
                SUM(ms.teleconsult) AS teleconsult
        FROM
            missions_select ms
        WHERE
            ms.user_id = {user_id}
        GROUP BY
            ms.user_id
        """
             },
            {'CONTENT_ETAB': """
             WITH
            missions_select AS (
                SELECT
                ua.candidate_id AS user_id,
                CASE WHEN go.establishment_type = 'clinic' THEN 1 ELSE 0 END AS clinic,
                CASE WHEN go.establishment_type = 'ehpad_rh' THEN 1 ELSE 0 END AS ehpad_rh,
                CASE WHEN go.establishment_type = 'had' THEN 1 ELSE 0 END AS had,
                CASE WHEN go.establishment_type = 'hea_cen' THEN 1 ELSE 0 END AS hea_cen,
                CASE WHEN go.establishment_type = 'hea_hou' THEN 1 ELSE 0 END AS hea_hou,
                CASE WHEN go.establishment_type = 'home_consult'  THEN 1 ELSE 0 END AS home_consult,
                CASE WHEN go.establishment_type = 'hospi' THEN 1 ELSE 0 END AS hospi,
                CASE WHEN go.establishment_type = 'labo' THEN 1 ELSE 0 END AS labo,
                CASE WHEN go.establishment_type = 'lib_off' THEN 1 ELSE 0 END AS lib_off,
                CASE WHEN go.establishment_type = 'other_ms' THEN 1 ELSE 0 END AS other_ms,
                CASE WHEN go.establishment_type = 'priv_comp'  THEN 1 ELSE 0 END AS priv_comp,
                CASE WHEN go.establishment_type = 'ssr'  THEN 1 ELSE 0 END AS ssr,
                CASE WHEN go.establishment_type = 'teleconsult'  THEN 1 ELSE 0 END AS teleconsult
                FROM
                medelse.announcement a
                JOIN medelse.user_announcement ua ON ua.announcement_id = a.id
                join medelse.group_office go on go.id = a.office_id
                WHERE
                a.created_at > '2023-01-01'
                AND
                ua.candidate_id = {user_id}
                AND
                    ua.read_at is not NULL
            )
            SELECT
                ms.user_id,
                SUM(ms.clinic) AS clinic,
                SUM(ms.ehpad_rh) AS ehpad_rh,
                SUM(ms.had) AS had,
                SUM(ms.hea_cen) AS hea_cen,
                SUM(ms.hea_hou) AS hea_hou,
                SUM(ms.home_consult) AS home_consult,
                SUM(ms.hospi) AS hospi,
                SUM(ms.labo) AS labo,
                SUM(ms.lib_off) AS lib_off,
                SUM(ms.other_ms) AS other_ms,
                SUM(ms.priv_comp) AS priv_comp,
                SUM(ms.ssr) AS ssr,
                SUM(ms.teleconsult) AS teleconsult
        FROM
            missions_select ms
        WHERE
              ms.user_id IS NOT NULL
        GROUP BY
            ms.user_id

        """
             },
            {'USER_SERVICE': """
            WITH
                missions_select AS (
            SELECT
                u.id AS user_id,
                us.created_at,
                CASE WHEN us.service_id = 11 THEN 1 ELSE 0 END AS biology,
                CASE WHEN us.service_id = 45 THEN 1 ELSE 0 END AS bloc_op,
                CASE WHEN us.service_id = 5 THEN 1 ELSE 0 END AS chirurgie,
                CASE WHEN us.service_id = 41 THEN 1 ELSE 0 END AS endocrino,
                CASE WHEN us.service_id = 4 THEN 1 ELSE 0 END AS geriatrie,
                CASE WHEN us.service_id = 28 THEN 1 ELSE 0 END AS medecine_generale,
                CASE WHEN us.service_id = 3 THEN 1 ELSE 0 END AS medecine_interne,
                CASE WHEN us.service_id = 42 THEN 1 ELSE 0 END AS medecine_specialite,
                CASE WHEN us.service_id = 30 THEN 1 ELSE 0 END AS reanimation,
                CASE WHEN us.service_id = 32 THEN 1 ELSE 0 END AS ssr,
                CASE WHEN us.service_id = 44 THEN 1 ELSE 0 END AS unite_de_soin,
                CASE WHEN us.service_id = 9 THEN 1 ELSE 0 END AS urgences
                FROM
                    medelse.user_service us
                    JOIN medelse.user u ON u.id = us.user_id
                    WHERE us.deleted_at is null
                    AND u.id = {user_id}
            )
            SELECT
            ms.user_id,
            SUM(ms.biology) AS biology,
            SUM(ms.bloc_op) AS bloc_op,
            SUM(ms.chirurgie) AS chirurgie,
            SUM(ms.endocrino) AS endocrino,
            SUM(ms.geriatrie) AS geriatrie,
            SUM(ms.medecine_generale) AS medecine_generale,
            SUM(ms.medecine_interne) AS medecine_interne,
            SUM(ms.medecine_specialite) AS medecine_specialite,
            SUM(ms.reanimation) AS reanimation,
            SUM(ms.ssr) AS ssr,
            SUM(ms.unite_de_soin) AS unite_de_soin,
            SUM(ms.urgences) AS urgences
            FROM
            missions_select ms
            WHERE
            ms.user_id IS NOT NULL
            GROUP BY
            ms.user_id
         """
             },
            {'CONTENT_SERVICE': """
                    WITH
            missions_select AS (
                SELECT
                ua.candidate_id AS user_id,
                CASE WHEN a.service_id = 11 AND ua.read_at IS NOT NULL THEN 1 ELSE 0 END AS biology,
                CASE WHEN a.service_id = 45 AND ua.read_at IS NOT NULL THEN 1 ELSE 0 END AS bloc_op,
                CASE WHEN a.service_id = 5 AND ua.read_at IS NOT NULL THEN 1 ELSE 0 END AS chirurgie,
                CASE WHEN a.service_id = 41 AND ua.read_at IS NOT NULL THEN 1 ELSE 0 END AS endocrino,
                CASE WHEN a.service_id = 4 AND ua.read_at IS NOT NULL THEN 1 ELSE 0 END AS geriatrie,
                CASE WHEN a.service_id = 28 AND ua.read_at IS NOT NULL THEN 1 ELSE 0 END AS medecine_generale,
                CASE WHEN a.service_id = 3 AND ua.read_at IS NOT NULL THEN 1 ELSE 0 END AS medecine_interne,
                CASE WHEN a.service_id = 42 AND ua.read_at IS NOT NULL THEN 1 ELSE 0 END AS medecine_specialite,
                CASE WHEN a.service_id = 30 AND ua.read_at IS NOT NULL THEN 1 ELSE 0 END AS reanimation,
                CASE WHEN a.service_id = 32 AND ua.read_at IS NOT NULL THEN 1 ELSE 0 END AS ssr,
                CASE WHEN a.service_id = 44 AND ua.read_at IS NOT NULL THEN 1 ELSE 0 END AS unite_de_soin,
                CASE WHEN a.service_id = 9 AND ua.read_at IS NOT NULL THEN 1 ELSE 0 END AS urgences
                FROM
                medelse.announcement a
                JOIN medelse.user_announcement ua ON ua.announcement_id = a.id
                WHERE
                a.created_at > '2023-01-01'
                AND
                ua.candidate_id = {user_id}
            )
            SELECT
            ms.user_id,
            SUM(ms.biology) AS biology,
            SUM(ms.bloc_op) AS bloc_op,
            SUM(ms.chirurgie) AS chirurgie,
            SUM(ms.endocrino) AS endocrino,
            SUM(ms.geriatrie) AS geriatrie,
            SUM(ms.medecine_generale) AS medecine_generale,
            SUM(ms.medecine_interne) AS medecine_interne,
            SUM(ms.medecine_specialite) AS medecine_specialite,
            SUM(ms.reanimation) AS reanimation,
            SUM(ms.ssr) AS ssr,
            SUM(ms.unite_de_soin) AS unite_de_soin,
            SUM(ms.urgences) AS urgences
            FROM
            missions_select ms
            WHERE
            ms.user_id IS NOT NULL
            GROUP BY
            ms.user_id
         """
             },
            {'CONTENT_RYTHME': """
                    WITH missions_select AS (
                SELECT
                ua.candidate_id AS user_id,
                CASE
                    WHEN a.tags::TEXT LIKE '%Announcement.Rhythm.Day%' THEN 1
                    ELSE 0
                END AS DAY,
                CASE
                    WHEN a.tags::TEXT LIKE '%Announcement.Rhythm.Night%' THEN 1
                    ELSE 0
                END AS night
                FROM
                medelse.announcement a
                JOIN medelse.user_announcement ua ON ua.announcement_id = a.id
                WHERE
                a.created_at > '2023-01-01'
                AND ua.read_at is not NULL
                AND ua.candidate_id = {user_id}
            )
            SELECT
            ms.user_id,
            SUM(ms.day) AS DAY,
            SUM(ms.night) AS night
            FROM
            missions_select ms
            WHERE
            ms.user_id IS NOT NULL
            GROUP BY
            ms.user_id
        """
             },
        ]
        cursor = connect.cursor(cursor_factory=RealDictCursor)
        sql_query = sql_queries[idx][data_type].format(user_id=user_id)
        cursor.execute(sql_query)
        response = cursor.fetchall()
        df = pd.DataFrame(response)
        return (df)
    except psycopg2.ProgrammingError as e:
        return ("Error during connection or querying to PostgreSQL:",  e)
    finally:
        cursor.close()
        connect.close()
