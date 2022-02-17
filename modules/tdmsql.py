import re

def tdmGetMaxListID(cnxn):
    cursor = cnxn.cursor()
    cursor.execute("Select max(LISTID) from TDM_LIST;")
    maxid = str(cursor.fetchall())
    maxid = re.sub('[^A-Za-z0-9]+', '', maxid)
    maxid = int(maxid) + 1
    maxid = str(maxid)
    while len(maxid) < 7:
        maxid = '0' + maxid
    return maxid

def get_next_pos_for_logfile(cnxn, listid):
    cursor = cnxn.cursor()
    cursor.execute("SELECT MAX(POS)\
  FROM TMS_CHANGEINFO\
  WHERE ID = '%s' AND TNAME = 'TDM_LIST'" % listid)
    next_pos = str(cursor.fetchall())
    next_pos = re.sub('[^0-9]+', '', next_pos)
    if next_pos == '':
        next_pos = 0
    next_pos = int(next_pos) + 1
    return next_pos


def tdmGetUserName(cnxn, userID):
    cursor = cnxn.cursor()
    cursor.execute("SELECT [FIRSTNAME] FROM TMS_USER WHERE USERNAME = '%s'" % (userID))
    firstname = str(cursor.fetchall())
    firstname = re.sub('[^A-Za-z0-9]+', '', firstname)
    cursor.execute("SELECT [NAME] FROM TMS_USER WHERE USERNAME = '%s'" % (userID))
    lastname = str(cursor.fetchall())
    lastname = re.sub('[^A-Za-z0-9]+', '', lastname)
    username = firstname + " " + lastname
    return username


def tdmGetCompsID(cnxn, d2list):
    cursor = cnxn.cursor()
    clist = []
    for d2 in d2list:
        cursor.execute("SELECT [COMPID] FROM TDM_COMP WHERE NAME2 = '%s'" % (d2))
        compid = str(cursor.fetchall())
        compid = re.sub('[^\w+]', '', compid)
        clist.append(compid)
    return clist

def tdmGetUsedMaterial(cnxn):
    pattern = re.compile(r'\'\w+\'')
    mat_list = []
    cursor = cnxn.cursor()
    cursor.execute("SELECT DISTINCT [MATERIALID] FROM TDM_LIST")
    data = cursor.fetchall()
    for ele in data:
        ele = pattern.findall(str(ele))
        ele = re.sub('[^\w -_,.]+', '', ele[0])
        mat_list.append(ele)
    return mat_list


def tdmGetAllMaterial(cnxn): #not working
    pattern = re.compile(r'\'\w+\'')
    mat_list = []
    cursor = cnxn.cursor()
    cursor.execute("SELECT DISTINCT [MATERIALID] FROM TDM_LIST")
    data = cursor.fetchall()
    for ele in data:
        ele = pattern.findall(str(ele))
        ele = re.sub('[^\w -_,.]+', '', ele[0])
        mat_list.append(ele)
    return mat_list

#THIS IS 
#THE ONE THAT WORKS WITH GUI
#AND CREATES TUPLE FOR TREEVIEW
def tdm_get_list_tuple_test_db(cnxn):
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM dbo.GENERIC1")
    data = cursor.fetchall()
    new_data = []
    for toople in data:
        new_toople_ele = []
        for ele in toople:
            ele = re.sub('[^\w -_,.]+', '', str(ele))
            new_toople_ele.append(ele)
        new_data.append(new_toople_ele)
    return new_data
    
def tdm_get_list_tuple_TDM_LIST(cnxn):
    cursor = cnxn.cursor()
    cursor.execute("SELECT [LISTID], [NCPROGRAM], [PARTNAME] FROM TDM_LIST")
    data = cursor.fetchall()
    new_data = []
    for toople in data:
        new_toople_ele = []
        for ele in toople:
            ele = re.sub('[^\w -_,.]+', '', str(ele))
            new_toople_ele.append(ele)
        new_data.append(new_toople_ele)
    return new_data

def tdm_get_list_tuple_material_used(cnxn):
    cursor = cnxn.cursor()
    cursor.execute("SELECT DISTINCT MATERIALID FROM TDM_LIST")
    material_ids = cursor.fetchall()
    material_ids_string = ""
    mat = re.findall(r'\'.+\'', str(material_ids[0]))
    for mat_id in material_ids:
        mat = re.findall(r'\'.+\'', str(mat_id))
        if mat != []:
            material_ids_string = material_ids_string + mat[0] + ","
    final_string = ""
    for i, char in enumerate(material_ids_string):
        if i < len(material_ids_string) - 1:
            final_string = final_string + char
    cursor.execute("SELECT [MATERIALID], [NAME] FROM TDM_MATERIAL\
        WHERE MATERIALID IN (%s)" % final_string)
    data = cursor.fetchall()
    new_data = []
    for toople in data:
        new_toople_ele = []
        for ele in toople:
            ele = re.sub('[^\w -_,.]+', '', str(ele))
            new_toople_ele.append(ele)
        new_data.append(new_toople_ele)
    return new_data
    
def tdm_get_list_tuple_TDM_MATERIAL(cnxn):
    cursor = cnxn.cursor()
    cursor.execute("SELECT [MATERIALID], [NAME] FROM TDM_MATERIAL")
    data = cursor.fetchall()
    new_data = []
    for toople in data:
        new_toople_ele = []
        for ele in toople:
            ele = re.sub('[^\w -_,.]+', '', str(ele))
            new_toople_ele.append(ele)
        new_data.append(new_toople_ele)
    return new_data
        
def tdm_get_list_tuple_TDM_MACHINE(cnxn):
    cursor = cnxn.cursor()
    cursor.execute("SELECT [MACHINEID], [NAME], [MACHINEGROUPID] FROM TDM_MACHINE")
    data = cursor.fetchall()
    new_data = []
    for toople in data:
        new_toople_ele = []
        for ele in toople:
            ele = re.sub('[^\w -_,.]+', '', str(ele))
            new_toople_ele.append(ele)
        new_data.append(new_toople_ele)
    return new_data

def tdm_get_MACHINEGROUPID_by_MACHINEID(cnxn, machine):
    pattern = re.compile(r'\'[_ \w]+\'')
    cursor = cnxn.cursor()
    cursor.execute("SELECT MACHINEGROUPID FROM TDM_MACHINE\
        WHERE MACHINEID = '%s'" % machine)
    machinegroupid = cursor.fetchall()
    machinegroupid = pattern.findall(str(machinegroupid[0]))
    machinegroupid = re.sub('[^\w -_,.]+', '', str(machinegroupid[0]))
    machinegroupid = re.sub('\'', '', machinegroupid)
    print(machinegroupid)
    return machinegroupid

def tdm_get_list_tuple_fixture_used(cnxn):
    cursor = cnxn.cursor()
    cursor.execute("SELECT DISTINCT FIXTURE FROM TDM_LIST")
    data = cursor.fetchall()
    new_data = []
    for toople in data:
        new_toople_ele = []
        for ele in toople:
            ele = re.sub('[^\w -_.,]+', '', str(ele))
            new_toople_ele.append(ele)
        new_data.append(new_toople_ele)
    return new_data
    
'''def tdm_get_list_tuple_TDM_FIXTURE(cnxn):
    cursor = cnxn.cursor()
    cursor.execute("SELECT [FIXTUREID], [FIXTURENAME], [FIXTURENAME2] FROM TDM_FIXTURE")
    data = cursor.fetchall()
    new_data = []
    for toople in data:
        new_toople_ele = []
        for ele in toople:
            ele = re.sub('[^\w -_.,]+', '', str(ele))
            new_toople_ele.append(ele)
        new_data.append(new_toople_ele)
    return new_data'''

def tdmCheckIfToolsExists(cnxn, tlist):
    valid = True
    cursor = cnxn.cursor()
    for tool in tlist:
        cursor.execute("SELECT TOOLID FROM TDM_TOOL WHERE TOOLID = '%s'" % (tool))
        output = str(cursor.fetchall())
        output = re.sub('[^\w -_,.]+', '', output)
        if output == "":
            valid = False
    return valid

def tdmCheckIfCompExists(cnxn, tlist):
    valid = True
    cursor = cnxn.cursor()
    for tool in tlist:
        cursor.execute("SELECT COMPID FROM TDM_COMP WHERE COMPID = '%s'" % (tool))
        output = str(cursor.fetchall())
        output = re.sub('[^\w -_,.]+', '', output)
        if output == "":
            valid = False
    return valid


def tdm_list_missing_tools(cnxn, tlist):
    cursor = cnxn.cursor()
    bad_list = list()
    for tool in tlist:
        cursor.execute("SELECT TOOLID FROM TDM_TOOL WHERE TOOLID = '%s'" % (tool))
        output = str(cursor.fetchall())
        output = re.sub('[^\w -_,.]+', '', output)
        if output == "":
            bad_list.append(tool)
    return bad_list

def tdm_list_missing_comps(cnxn, tlist):
    cursor = cnxn.cursor()
    bad_list = list()
    for tool in tlist:
        cursor.execute("SELECT COMPID FROM TDM_COMP WHERE NAME2 = '%s'" % (tool))
        output = str(cursor.fetchall())
        output = re.sub('[^\w -_,.]+', '', output)
        if output == "":
            bad_list.append(tool)
    return bad_list


def tdmListCheckbyNC(cnxn, NCprogram):
    cursor = cnxn.cursor()
    cursor.execute("SELECT LISTID FROM TDM_LIST WHERE NCPROGRAM = '%s'" % (NCprogram))
    output = str(cursor.fetchall())
    output = re.sub('[^\w -_,.]+', '', output)
    if output == "":
        return False
    else:
        return True


def tdmCreateList(cnxn, NCprogram, maxid, user, timestamp):
    cursor = cnxn.cursor()
    #cursor.execute("insert into TDM_LIST (TIMESTAMP, LISTID, NCPROGRAM, PARTNAME, PARTNAME01, WORKPIECEDRAWING, JOBPLAN, WORKPROCESS, MATERIALID, MACHINEID, MACHINEGROUPID, FIXTURE, NOTE, NOTE01, WORKPIECECLASSID, STATEID1, STATEID2, LISTTYPE, USERNAME, ACCESSCODE) values (1628337607, N'0002712', N'5555555', null, null, null, null, null, null, null, null, null, null, null, null, N'TOOL LIST IS PREPARING', null, 2, null, null)")
    cursor.execute("insert into TDM_LIST (TIMESTAMP, LISTID, NCPROGRAM, PARTNAME, PARTNAME01, WORKPIECEDRAWING, JOBPLAN, WORKPROCESS, MATERIALID, MACHINEID, MACHINEGROUPID, FIXTURE, NOTE, NOTE01, WORKPIECECLASSID, STATEID1, STATEID2, LISTTYPE, USERNAME, ACCESSCODE) values (%d, N'%s', N'%s', null, null, N'%s', null, null, null, null, null, null, null, null, null, N'TOOL LIST IS PREPARING', null, 2, N'%s', null)" % (timestamp, maxid, NCprogram, maxid, user))
    cnxn.commit()

def tdmCreateListTLM2(cnxn, timestamp, listid, ncprogram, desc, material, machine, machinegroup, fixture, listtype, username):
    parameters = [timestamp, listid, ncprogram, desc, material, machine, machinegroup, fixture, listtype, username]
    params_formatted = []
    for param in parameters:
        if param != "null":
            params_formatted.append("\'" + str(param) + "\'")
        else:
            params_formatted.append(param)
    timestamp = params_formatted[0]
    listid = params_formatted[1]
    ncprogram = params_formatted[2]
    desc = params_formatted[3]
    material = params_formatted[4]
    machine = params_formatted[5]
    machinegroup = params_formatted[6]
    fixture = params_formatted[7]
    listtype = params_formatted[8]
    username = params_formatted[9]
    print("insert into TDM_LIST (TIMESTAMP, LISTID, NCPROGRAM, PARTNAME, PARTNAME01, WORKPIECEDRAWING, JOBPLAN, WORKPROCESS, MATERIALID, MACHINEID, MACHINEGROUPID, FIXTURE, NOTE, NOTE01, WORKPIECECLASSID, STATEID1, STATEID2, LISTTYPE, USERNAME, ACCESSCODE) \
        values (%s, %s, %s, %s, null, %s, null, null, %s, %s, %s, %s, null, null, null, 'TOOL LIST IS PREPARING', null, %s, %s, null)"\
             % (timestamp, listid, ncprogram, desc, listid, material, machine, machinegroup, fixture, listtype, username))

    cursor = cnxn.cursor()
    #cursor.execute("insert into TDM_LIST (TIMESTAMP, LISTID, NCPROGRAM, PARTNAME, PARTNAME01, WORKPIECEDRAWING, JOBPLAN, WORKPROCESS, MATERIALID, MACHINEID, MACHINEGROUPID, FIXTURE, NOTE, NOTE01, WORKPIECECLASSID, STATEID1, STATEID2, LISTTYPE, USERNAME, ACCESSCODE) values (1628337607, N'0002712', N'5555555', null, null, null, null, null, null, null, null, null, null, null, null, N'TOOL LIST IS PREPARING', null, 2, null, null)")
    cursor.execute("insert into TDM_LIST (TIMESTAMP, LISTID, NCPROGRAM, PARTNAME, PARTNAME01, WORKPIECEDRAWING, JOBPLAN, WORKPROCESS, MATERIALID, MACHINEID, MACHINEGROUPID, FIXTURE, NOTE, NOTE01, WORKPIECECLASSID, STATEID1, STATEID2, LISTTYPE, USERNAME, ACCESSCODE) \
        values (%s, %s, %s, %s, null, %s, null, null, %s, %s, %s, %s, null, null, null, 'TOOL LIST IS PREPARING', null, %s, %s, null)"\
             % (timestamp, listid, ncprogram, desc, listid, material, machine, machinegroup, fixture, listtype, username))
    cnxn.commit()



def tdmCreateListMLCUBE(cnxn, NCprogram, maxid, user, timestamp):
    cursor = cnxn.cursor()
    #cursor.execute("insert into TDM_LIST (TIMESTAMP, LISTID, NCPROGRAM, PARTNAME, PARTNAME01, WORKPIECEDRAWING, JOBPLAN, WORKPROCESS, MATERIALID, MACHINEID, MACHINEGROUPID, FIXTURE, NOTE, NOTE01, WORKPIECECLASSID, STATEID1, STATEID2, LISTTYPE, USERNAME, ACCESSCODE) values (1628337607, N'0002712', N'5555555', null, null, null, null, null, null, null, null, null, null, null, null, N'TOOL LIST IS PREPARING', null, 2, null, null)")
    cursor.execute("insert into TDM_LIST (TIMESTAMP, LISTID, NCPROGRAM, PARTNAME, PARTNAME01, WORKPIECEDRAWING, JOBPLAN, WORKPROCESS, MATERIALID, MACHINEID, MACHINEGROUPID, FIXTURE, NOTE, NOTE01, WORKPIECECLASSID, STATEID1, STATEID2, LISTTYPE, USERNAME, ACCESSCODE) values (%d, N'%s', N'%s', null, null, N'%s', null, null, null, N'MMLCUBEB', N'STANDALONE', null, null, null, null, N'TOOL LIST IS PREPARING', null, 2, N'%s', null)" % (timestamp, maxid, NCprogram, maxid, user))
    cnxn.commit()

def tdmDeleteListbyNC(cnxn, NCprogram):
    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM TDM_LIST WHERE NCPROGRAM = '%s'" % (NCprogram))
    cnxn.commit()


def tdmAddTools(cnxn, listID, tlist, timestamp):
    i = 1
    cursor = cnxn.cursor()
    for tool in tlist:
        cursor.execute("INSERT INTO TDM_LISTLISTB VALUES ('%s', %d, NULL, '%s', NULL, NULL, NULL, '%s', NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, %d)" % (listID, i, tool, tool, timestamp))
        cnxn.commit()
        i += 1


def tdmAddComps(cnxn, listID, clist, timestamp):
    i = 1
    cursor = cnxn.cursor()
    #print(clist)
    for tool in clist:
        #print("INSERT INTO TDM_LISTLISTB VALUES ('%s', %d, '%s', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, %d)" % (listID, i, tool, timestamp))
        cursor.execute("INSERT INTO TDM_LISTLISTB VALUES ('%s', %d, '%s', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, %d)" % (listID, i, tool, timestamp))
        cnxn.commit()
        i += 1

    

def tdmAddLogfile(cnxn, listid, user, timestamp, pos, changedate, changetime):
    cursor = cnxn.cursor()
    #cursor.execute("INSERT INTO TMS_CHANGEINFO (TIMESTAMP, TNAME, ID, ID2, ID3, ID4, ID5, POS, USERID, NOTE, CHANGEDATE, CHANGETIME, CREATIONTIMESTAMP) VALUES (1628337608, N'TDM_LIST', N'0002712',null ,null ,null ,null ,1, N'PIETRZYK_P ,null ,153986, 50408, 1628337608)")
    cursor.execute("INSERT INTO TMS_CHANGEINFO (TIMESTAMP, TNAME, ID, ID2, ID3, ID4, ID5, POS, USERID, NOTE, CHANGEDATE, CHANGETIME, CREATIONTIMESTAMP) VALUES (%d , 'TDM_LIST', '%s',null ,null ,null ,null , %d, '%s','Lista stworzona automatycznie za pomocą programu Tool List Maker' ,%d, %d, %d)" % (timestamp, listid, pos, user, changedate, changetime, timestamp))
    cnxn.commit()

def tdmDisconnect(cnxn):
    cnxn.close()

def tdm_update_list(cnxn, timestamp, listid, ncprogram, desc, material, machine, machinegroup, fixture, listtype, username):
    if ncprogram != False:
        if ncprogram != "null":
            ncprogram = ", NCPROGRAM = '%s'" % ncprogram
        else:
            ncprogram = ", NCPROGRAM = NULL"
    else:
        ncprogram = ""

    if desc != False:
        if desc != "null":
            desc = ", PARTNAME = '%s'" % desc
        else:
            desc = ", PARTNAME = NULL"
    else:
        desc = ""

    if material != False:
        if material != "null":
            material = ", MATERIALID = '%s'" % material
        else:
            material = ", MATERIALID = NULL"
    else:
        material = ""

    if machine != False:
        if machine != "null":
            machine = ", MACHINEID = '%s'" % machine
        else:
            machine = ", MACHINEID = NULL"
    else:
        machine = ""

    if machinegroup != False:
        if machinegroup != "null":
            machinegroup = ", MACHINEGROUPID = '%s'" % machinegroup
        else:
            machinegroup = ", MACHINEGROUPID = NULL"
    else:
        machinegroup = ""

    if fixture != False:
        if fixture != "null":
            fixture = ", FIXTURE = '%s'" % fixture
        else:
            fixture = ", FIXTURE = NULL"
    else:
        fixture = ""

    if listtype != False:
        listtype = ", LISTTYPE = %d" % listtype
    else:
        listtype = ""


    cursor = cnxn.cursor()
    cursor.execute("UPDATE TDM_LIST\
        SET TIMESTAMP = %s%s%s%s%s%s%s%s, USERNAME = '%s'\
        WHERE LISTID = %s" % (timestamp, ncprogram, desc, material, machine, machinegroup, fixture, listtype, username, listid))

def tdm_delete_list_positions(cnxn, listid):
    cursor = cnxn.cursor()
    cursor.execute("DELETE TDM_LISTLISTB\
    WHERE LISTID = '%s'" % listid)
    cursor.commit()

def validate_list_ID(cnxn, list_ID):
    cursor = cnxn.cursor()
    cursor.execute("SELECT LISTID FROM TDM_LIST \
WHERE LISTID = '%s'" % list_ID)
    output = str(cursor.fetchall())
    output = re.sub('[^\w -_,.]+', '', output)
    if output == "":
        return False
    else:
        return True

def validate_machine(cnxn, machine_ID):
    cursor = cnxn.cursor()
    cursor.execute("SELECT MACHINEID FROM TDM_MACHINE \
WHERE MACHINEID = '%s'" % machine_ID)
    output = str(cursor.fetchall())
    output = re.sub('[^\w -_,.]+', '', output)
    if output == "":
        return False
    else:
        return True

def validate_material(cnxn, material_ID):
    cursor = cnxn.cursor()
    cursor.execute("SELECT MATERIALID FROM TDM_MATERIAL \
WHERE MATERIALID = '%s'" % material_ID)
    output = str(cursor.fetchall())
    output = re.sub('[^\w -_,.]+', '', output)
    if output == "":
        return False
    else:
        return True
