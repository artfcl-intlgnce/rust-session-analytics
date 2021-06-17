


data_list =  ['86975058', '589771454', '179051765', '397249863', '942837765', '3901070', '80085122', '241883428', '376270189', '915209455', '731735294', '2818751', '3721230', '432808995', '881446461', '893005834', '893005836', '893005839', '893005841', '57318134', '992939439', '283274328', '925505750', '973964104', '988402010', '995071880', '895231962', '993674321', '996548971', '990028854', '924613977', '978668746', '902545246', '911739032', '930791007', '985410467', '990249310', '924236183', '1462142', '893698611', '942945522', '52925646', '254871479', '983220024', '3114985', '445377422', '895492335', '896026775', '948506939', '977909216', '988676753', '992979540', '992979548', '992980340', '995950267', '842821132', '956319018', '1851412', '70200713', '206376668', '306403641', '307032295', '660169304', '714318322', '918960206', '920172179', '921857852', '925749944', '939163130', '952801475', '960411874', '968398355', '969861942', '972092532', '981660108', '983414161', '984468087', '988887073', '991187168', '992042263', '994900628', '996379064', '997181389', '995993282', '956182964', '996997478', '962464720', '996616045', '915807938', '695904652', '917278546', '996190129', '996190131', '988639861', '961167302', '759365847', '992879291', '927654032', '897281533', '895132194', '903301310', '905103082', '52002', '912563385', '997047735', '654443201', '915148534', '922201511', '895844542', '930895650', '897449318', '978951787', '130367282', '353543360', '894581064', '995329524', '335452753', '979660539', '992455950', '960358330', '362453554', '990397038', '218273140', 
'995413057', '36936547', '918830105', '918830109', '997098457', '166712453', '989060559', '64179496', '894868921', '896379630', '981429687', '962779554', '943127777', '977040938', '591594566', '892819088', '757542898', '979519640', '996641293', '879719005', '1857452', '992409558', '996962597', '987573940', '981179407', '921252561', '987783885', '981055111', '979680020', '528875687', '604270915', '905211990', '995272161', '906722871', '265235803', '918924825', '918970921', '918972107', '919289345', '997212644', '977086024', '980989758', '988448450', '993062785', '945852924', '994824117', '102993365', '3678847', '354041464', '987267610', '924341539', '645634020', '23245039', '908384754', '810139903', '893658509', '969008334', '969704114', '976556195', '977616975', '978836376', '982486035', '898328713', '990169892', '968085741', '997135172', '977595193', '898364976', '128309331', '990932067', '896988402', '981488497', '977241680', '947104096', '994310847', '139066533', '996178148', '996448852', '585030607', '963416551', '3170631', '855069239', '945706353', '207732347', '971753534', '351934137', '600328285', '893729781', '972216500', '993635354', '269453448', '941838978', '944586180', '997232361', '909124127', '872556231', '996416269', '981692422', '1310485', '997197591', '997232791', '925643630', '903651026', '922471466', '994026202', '974850502', '411863280', '672502295', '896050418', '289097763', '308141845', '995406550', '182543206', '929143563', '974616117', '264678220', '963754257', '490566287', '932492647', '994662014', '997031226', '184659983', '997232783', '992377027', '985967323', '290264346', '996213671', '167712053', '766307301', '710775488', '3010118', '321001614', '895375528', '937983122', '983014492', '960888745', '984927943', '967897225', '997232780', '600809163', '901239357', '962315759', '979207452', '897798944', '996664136', '997232779', '562882372', '898365783', '205263307', '895034580', '923736321', '940458423', '121310521', '663551343', '923604890', '991292477', '995106033', '189042391', '987067164', '996768934', '997153148', '997218939', '898139631', '889942894', '730129481', '966316336', '3078075', '215042271', '568134', '897137952', '667273938', '997232775', '214737', '861626930', '997029404', '893223810', '996884419', '240333770', '895102593', '996973395', '997157978', '997232772', '997232773', '997232774', '198873595', '992933079', '964623975', '59184863', '994565139', '395343867', '934929887', '971814981', '978932501', '968359351', '991206746', '89648533', '198293170', '813729901', '895198760', '896063914', '903078446', '926350525', '968572478', '994324612', '994589771', '997125034', '997225316', '921614274', '599070758', '3687421', '368932305', '771036488', '951908622', '978187445', '980100630', '923350232', '997232771', '987483165', '997232770', '90721756', '894293325', '895963449', '968409982', '968527386', '989250745', '893880097', '14299015', '189361988', '988558773', '100496031', '166900519', '797538098', '956921419', '156956207', '797310599', '995204775', '997201119', '578325146', '892901765', '996936219', '34563', '955818125', '927417585', '777831646', '995828134', '983824061', '900757544', '901561336', '997091375', '997232769', '182016526', '672451306', '539369529', '989123691', '978028502', '458847234', '582072325', '245118849', '941449162', '995691891', '983980354', '963473764', '995945637', '297670296', '840698729', '897369661', '967279844', '995589712', '997219075', '978292129', '997232768', '720605333', '926261517', '933557891', '936802554', '284567652', '356959862']

data_set = set(data_list)
contains_duplicates = len(data_list) != len(data_set)
print(str(contains_duplicates))
print(str(len(data_list)))