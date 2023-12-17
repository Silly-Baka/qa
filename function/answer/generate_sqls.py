


def generate_sql(data):
    args = data['args']
    sqls = []
    for quetions in data['question_types']:
        sql = []
        if quetions == 'fund_UNcompany':
            sql = [
                "MATCH(m:fund)-[r:fund2company]->(n:company) where m.name='{0}' return n.name, m.name".format(i)
                for i in args.keys()]
        elif quetions == 'company_UNfund':
            sql = [
                "MATCH(m:fund)-[r:fund2company]->(n:company) where n.name='{0}' return n.name, m.name".format(i)
                for i in args.keys()]
        elif quetions == 'fund_UNscale':
            sql = [
                "MATCH(m:fund)-[r:fund2scale]->(n:scale) where m.name='{0}' return n.name, m.name".format(i)
                for i in args.keys()]
        elif quetions == 'fund_UNindex':
            sql = [
                "MATCH(m:fund)-[r:fund2index]->(n:index) where m.name='{0}' return n.name, m.name  ".format(i)
                for i in args.keys()]
        elif quetions == 'index_UNfund':
            sql = [
                "MATCH(m:fund)-[r:fund2index]->(n:index) where n.name='{0}' return n.name, m.name".format(i)
                for i in args.keys()]
        elif quetions == 'fund_UNmanager':
            sql = [
                "MATCH(m:fund)-[r:fund2manager]->(n:manager) where m.name='{0}' return n.name, m.name ".format(i)
                for i in args.keys()]
        elif quetions=='manage_UNfund':
            sql = [
                "MATCH(m:fund)-[r:fund2manager]->(n:manager) where n.name='{0}' return n.name, m.name".format(i)
                for i in args.keys()]
        if sql :
            sqls.append({'question_type': quetions, 'sql': sql})
            # print('sqls:', sqls)
    return sqls