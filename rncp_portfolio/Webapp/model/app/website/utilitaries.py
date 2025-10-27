import psycopg2


def db_connector():

    conn = psycopg2.connect(
        host="localhost",
        dbname="medelse",
        user="tristan",
        password=""
    )

    return (conn)


def normalize_model_output(raw_output):
    if isinstance(raw_output, str):
        return {"error": raw_output}

    if not raw_output:
        return []

    formatted = []

    for entry in raw_output:
        if isinstance(entry, str):
            return {"error": entry}

        try:
            *category_groups, final_score = entry

            formatted_categories = []
            for categories in category_groups:
                for c in categories:
                    if isinstance(c, (tuple, list)) and len(c) >= 2:
                        formatted_categories.append({
                            "name": c[0],
                            "score": float(c[1])
                        })
                    elif isinstance(c, str):
                        formatted_categories.append({
                            "name": c,
                            "score": 0.0
                        })

            formatted.append({
                "final_score": float(final_score),
                "categories": formatted_categories
            })

        except Exception as e:
            print("❌ Error normalizing:", entry, e)

    return formatted
