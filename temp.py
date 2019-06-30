def main(req: func.HttpRequest) -> func.HttpResponse:

    # FTP Server parameters
    USERNAME = "expertimeftp"
    PASWORD = """&A)5qvL"9/,@m-A{j|v^7zt \}:GkYEyk&=WRkwhl]v|.'T!8:~AkRT}di:;rOv1"""
    SERVER = '212.155.230.205'

    import_count = 0

    # if a file name is obtained then start the process
    if True:

        # arrays with the list of processed and input files
        raw_data_array = []
        processed_array = []

        # workaround to set pysftp up and running on Python 3
        # and avoid "AttributeError: 'Connection' object has no attribute '_sftp_live'"
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        # establish a connection to the SFTP server
        with pysftp.Connection(host=SERVER, username=USERNAME, password=PASWORD, cnopts=cnopts) as sftp:
            logging.info("SFTP Connection succesfully established ... ")
            
            # Switch to a remote directory
            sftp.cwd('/PROCESSED')
            # Obtain structure of the remote directory '/var/www/vhosts'
            directory_structure = sftp.listdir_attr()
            # Get filenames
            for attr in directory_structure:
                fname = os.path.splitext(attr.filename)[0]
                # initialized processed dataset
                processed_array.append(fname)
            
            # Some other example server values are
            # server = 'localhost\sqlexpress' # for a named instance
            # server = 'myserver,port' # to specify an alternate port
            server = 'tcp:clixsql01.database.windows.net' 
            database = 'E-BTS' 
            username = 'btsadmin' 
            password = '9M=!d_pxB5' 
            cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
            cursor = cnxn.cursor()

            # now get the initial data
            sftp.cwd('/RAWDATA')
            # Obtain structure of the remote directory '/var/www/vhosts'
            directory_structure = sftp.listdir_attr()
            # Print data
            for attr in directory_structure:
                fname = os.path.splitext(attr.filename)[0]
                extension = os.path.splitext(attr.filename)[1]
                if str(extension) == '.pdf':
                    raw_data_array.append(fname)

            # get all the files from RAWDATA that have not been processed yet 
            difference_array = list(set(raw_data_array) - set(getImportFiles(cursor)))
            logging.info('############################################')
            logging.info(difference_array)
            for unprocessed_file in difference_array:
                # create file object from a file name (obtained from the GET request) to read the file directly to a variable
                file_object = BytesIO()
                sftp.getfo(unprocessed_file+".pdf", file_object)
                images = convert_from_bytes(file_object.getvalue())
                # get a file name without extension
                clean_filename = unprocessed_file
                # first 4 digits is a postal code
                postcode = clean_filename[:6]
                school_name = ''
                school_level = ''
                _name = clean_filename[6:]
                _name.replace(' ', '-')
                for item in _name.split('-'):
                    if item.lower().startswith('cm') or item.lower().startswith('cp') or item.lower().startswith('ce'):
                        school_level += ' ' + item
                        break
                    else:
                        school_name += ' ' + item

                # insert into import data
                cursor.execute("insert into Import(postalcode, school, class, filename, isapproved) values (?, ?, ?, ?, ?)",  postcode, school_name, school_level, unprocessed_file, 0)
                cnxn.commit() 
                # right after insertion get import id
                import_id = get_id(cursor)
                       
                # points of interest from all the pages
                global_poi = []
                # create a byte array for each page
                for image in images:
                    byte_array = pil_to_array(image)
                    page_poi = image_to_text(byte_array)
                    global_poi += page_poi
                items = global_poi
                # do text preprocessing
                dictionary = ['équerre', 'xl', 'vues', 'vives', 'violet', 'vert', 'velleda', 'uni', 'trieur', 'tipp', 'taille', 'surligneurs', 'stylos',
                                'stylo', 'simples', 'seyes', 'sey', 'réécriveurs', 'règle', 'rouleau', 'rouge', 'rose', 'remborde', 'rabats', 'protege',
                                'positions', 'polypro', 'pochettes', 'pochette', 'plastique', 'piqure', 'perforees', 'papier', 'orange', 'opaque',
                                'noir', 'lustree', 'livres', 'jaune', 'intercalaires', 'incolore', 'grip', 'gel', 'fluo', 'fiches', 'feutres',
                                'feuilles', 'exacompta', 'elastique', 'effaçable', 'effaceurs', 'décors', 'documents', 'crayons',
                                'crayon', 'couvre', 'couleurs', 'couleur', 'correcteurs', 'comfort', 'coloriage', 'cm', 'classeur', 'ciseaux',
                                'carte', 'carnet', 'cahier', 'bâtons', 'brillant', 'bleu', 'blanches', 'bille', 'gomme', 'ardoise', 
                                'cartouches', 'colle', 'chiffon', 'tubes', 'pinceaux', 'kleenex', 'livre', 'compas', 'décimètre', 'colles',
                                'trousse', 'critérium', 'mines', 'boîtes', 'mouchoirs', 'agenda', 'étui', 'mine', 'cartable']
                
                # Important lines with articles
                res = []
                # leave only important items
                for item in items:
                    #Remove punctuation / special characters '!\"#$%&\\'()*+,-./:;<=>?@[\\\\]^_`{|}~'
                    item = re.sub('[%s]' % re.escape(string.punctuation.replace('+', '')), ' ', item)
                    for word in item.split():
                        if word in dictionary:
                            res.append(item)
                result = IndexedSet(res)

                # Split by + delimiter
                res_after_split = []

                for line in result:
                    res_after_split += [str(element).strip()
                                        for element in re.split(' \+ | avec | et ', line)]
                #Remove empty string 
                res_after_split = filter(None, res_after_split)
                
                # Get Quantitiy/Article
                quantity = []
                article = []
                # if a lines start with a digit then quantity = digit
                # quantity = 1 otherwise
                for item in res_after_split:
                    first = item.split(' ',)[0]
                    if first.isnumeric():
                        quantity.append(first)
                    else:
                        quantity.append("1")
                    # article.append(item.replace(first,''))
                    article.append(item)
                df_list = zip(quantity, article)

                tuple_list = list(df_list)
                # convert to pandas dataframe
                pd.set_option('max_colwidth', 150)
                items_df = pd.DataFrame(tuple_list, columns=[
                                        'product_qty', 'user_request'])
                # remove empty string
                items_df['user_request'].replace('', np.nan, inplace=True)
                items_df.dropna(subset=['user_request'], inplace=True)
                output = []
                product_codes = []
                post_codes = []
                school_names = []
                school_levels = []

                for index, row in items_df.iterrows():
                    item = row['user_request']
                    quantity = row['product_qty']
                    product_code, product_name = get_scored_label(item)
                    output.append(str(product_name))
                    product_codes.append(str(product_code))
                    post_codes.append(postcode)
                    school_names.append(school_name)
                    school_levels.append(school_level)
                    # insert into retraining table
                    cursor.execute("insert into ReTrainingSet (postalcode, school, class, userrequest, productcode, quantity, productname, importid, isapproved) values (?, ?, ?, ?, ?, ?, ?, ?, ?)",  
                    postcode, school_name, school_level, item, product_code, quantity, product_name, import_id, 0)
                    cnxn.commit() 

        return func.HttpResponse(f"Success")
    else:
        return func.HttpResponse(
            "Please pass a file name on the query string or in the request body",
            status_code=400
        )
