import MySQLdb

def main():
	gde_fpkm="D:/bioaurora/data/normal_gde_fpkm"
	read_csv("bio","FPKM",gde_fpkm)

	ase="D:/bioaurora/data/normal_ase_count"
	#read_csv("bio","ASE",ase)

def read_csv(db_name,table_name,FILE):
	db = MySQLdb.connect("localhost", "root", "root", db_name, charset='utf8' )
	cursor = db.cursor()
	cursor.execute("DROP TABLE IF EXISTS "+table_name)

	with open(FILE,"r") as doc:
		headname_ls=doc.readline().strip("\n").split("\t")
		body=doc.readlines()
	
	headname=",".join(headname_ls)
	#headname_type=" CHAR(40) NOT NULL PRIMARY KEY,".join(headname_ls)+" CHAR(40)"
	headname_type=headname_ls[0]+" CHAR(40) NOT NULL PRIMARY KEY,"+" FLOAT,".join(headname_ls[1:])+" FLOAT"

	#cursor.execute("CREATE TABLE fpkm(dimen_1 FLOAT,dimen_2 FLOAT)")
	cursor.execute("CREATE TABLE "+table_name+"("+headname_type+")")

	for line in body:
		ls=line.strip("\n").split("\t")
		value="','".join(ls)
		value="'"+value+"'"
		#$sql = "INSERT INTO fpkm (firstname, lastname, email) VALUES ('John', 'Doe', 'john@example.com')";
		cursor.execute("INSERT INTO "+table_name+" ("+headname+") VALUES ("+value+")");
	cursor.close()
	
if __name__=="__main__":
	main()

