#!/usr/bin/env python

# --------------------------------------------------------
# Faster R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""
Demo script showing detections in sample images.

See README.md for installation instructions before running.
"""

import _init_paths
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import caffe, os, sys, cv2
import argparse

# CLASSES = ('__background__', # always index 0
#                          '_1', '_2', '_3', '_4',
#                          '_5', '_6', '_7', '_8', '_9',
#                          '_10', '_11', '_12','_13', '_14',
#                          '_15', '_16', '_17', '_18','_19',
#                          '_20', '_21', '_22', '_23','_24',
#                          '_25', '_26', '_27', '_28','_29',
#                          '_30', '_31', '_32', '_33','_34',
#                          '_35','_36','_37')
# CLASSES = ('__background__', # always index 0
#                          '_1', '_2', '_3', '_4',
#                          '_5', '_6', '_7', '_8', '_9',
#                          '_10', '_11', '_12','_13', '_14',
#                          '_15', '_16', '_17')

# CLASSES = ('__background__', # always index 0
#                   '_1' , '_2' , '_3' , '_4' ,
#                   '_5' , '_6' , '_7' , '_8' , '_9',
#                   '_10', '_11', '_12', '_13', '_14',
#                   '_15', '_16', '_17', '_18', '_19',
#                   '_20', '_21', '_22', '_23', '_100')

# CLASSES = ('__background__', # always index 0
#                           '_1' , '_2' , '_3' , '_4' ,
#                           '_5' , '_6' , '_7' , '_8' , '_9',
#                           '_10', '_11', '_12', '_13', '_14',
#                           '_15', '_16', '_17', '_18', '_19',
#                           '_20', '_21', '_22', '_23', '_24',
#                            '_25', '_26', '_27', '_28', '_29',
#                            '_30', '_31', '_32', '_33', '_34',
#                            '_35', '_36', '_37', '_38', '_39',
#                            '_40', '_41', '_42', '_43', '_44',
#                            '_45', '_46', '_47', '_100')

CLASSES = ('__background__', # always index 0
                '_1', '_2', '_3', '_4', '_5', 
                '_6', '_7', '_8', '_9', '_10', 
                '_11', '_12', '_13', '_14', '_15', 
                '_16', '_17', '_18', '_19', '_20', 
                '_21', '_22', '_23', '_24', '_25', 
                '_26', '_27', '_28', '_29', '_30', 
                '_31', '_32', '_33', '_34', '_35', 
                '_36', '_37', '_38', '_39', '_40', 
                '_41', '_42', '_43', '_44', '_45', 
                '_46', '_47', '_48', '_49', '_50', 
                '_51', '_52', '_53', '_54', '_55', 
                '_56', '_57', '_58', '_59', '_60', 
                '_61', '_62', '_63', '_64', '_65', 
                '_66', '_67', '_68', '_69', '_70', 
                '_71', '_72', '_73', '_74', '_75', 
                '_76', '_77', '_78', '_79', '_80', 
                '_81', '_82', '_83', '_84', '_85', 
                '_86', '_87', '_88', '_89', '_90', 
                '_91', '_92', '_93', '_94', '_95', 
                '_96', '_97', '_98', '_99', '_100', 
                '_101', '_102', '_103', '_104', '_105', 
                '_106', '_107', '_108', '_109', '_110', 
                '_111', '_112', '_113', '_114', '_115', 
                '_116', '_117', '_118', '_119', '_120', 
                '_121', '_122', '_123', '_124', '_125', 
                '_126', '_127', '_128', '_129', '_130', 
                '_131', '_132', '_133', '_134', '_135', 
                '_136', '_137', '_138', '_139', '_140', 
                '_141', '_142', '_143', '_144', '_145', 
                '_146', '_147', '_148', '_149', '_150', 
                '_151', '_152', '_153', '_154', '_155', 
                '_156', '_157', '_158', '_159', '_160', 
                '_161', '_162', '_163', '_164', '_165', 
                '_166', '_167', '_168', '_169', '_170', 
                '_171', '_172', '_173', '_174', '_175', 
                '_176', '_177', '_178', '_179', '_180', 
                '_181', '_182', '_183', '_184', '_185', 
                '_186', '_187', '_188', '_189', '_190', 
                '_191', '_192', '_193', '_194', '_195', 
                '_196', '_197', '_198', '_199', '_200', 
                '_201', '_202', '_203', '_204', '_205', 
                '_206', '_207', '_208', '_209', '_210', 
                '_211', '_212', '_213', '_214', '_215', 
                '_216', '_217', '_218', '_219', '_220', 
                '_221', '_222', '_223', '_224', '_225', 
                '_226', '_227', '_228', '_229', '_230', 
                '_231', '_232', '_233', '_234', '_235', 
                '_236', '_237', '_238', '_239', '_240', 
                '_241', '_242', '_243', '_244', '_245', 
                '_246', '_247', '_248', '_249', '_250', 
                '_251', '_252', '_253', '_254', '_255', 
                '_256', '_257', '_258', '_259', '_260', 
                '_261', '_262', '_263', '_264', '_265', 
                '_266', '_267', '_268', '_269', '_270', 
                '_271', '_272', '_273', '_274', '_275', 
                '_276', '_277', '_278', '_279', '_280', 
                '_281', '_282', '_283', '_284', '_285', 
                '_286', '_287', '_288', '_289', '_290', 
                '_291', '_292', '_293', '_294', '_295', 
                '_296', '_297', '_298', '_299', '_300', 
                '_301', '_302', '_303', '_304', '_305', 
                '_306', '_307', '_308', '_309', '_310', 
                '_311', '_312', '_313', '_314', '_315', 
                '_316', '_317', '_318', '_319', '_320', 
                '_321', '_322', '_323', '_324', '_325', 
                '_326', '_327', '_328', '_329', '_330', 
                '_331', '_332', '_333', '_334', '_335', 
                '_336', '_337', '_338', '_339', '_340', 
                '_341', '_342', '_343', '_344', '_345', 
                '_346', '_347', '_348', '_349', '_350', 
                '_351', '_352', '_353', '_354', '_355', 
                '_356', '_357', '_358', '_359', '_360', 
                '_361', '_362', '_363', '_364', '_365', 
                '_366', '_367', '_368', '_369', '_370', 
                '_371', '_372', '_373', '_374', '_375', 
                '_376', '_377', '_378', '_379', '_380', 
                '_381', '_382', '_383', '_384', '_385', 
                '_386', '_387', '_388', '_389', '_390', 
                '_391', '_392', '_393', '_394', '_395', 
                '_396', '_397', '_398', '_399', '_400', 
                '_401', '_402', '_403', '_404', '_405', 
                '_406', '_407', '_408', '_409', '_410', 
                '_411', '_412', '_413', '_414', '_415', 
                '_416', '_417', '_418', '_419', '_420', 
                '_421', '_422', '_423', '_424', '_425', 
                '_426', '_427', '_428', '_429', '_430', 
                '_431', '_432', '_433', '_434', '_435', 
                '_436', '_437', '_438', '_439', '_440', 
                '_441', '_442', '_443', '_444', '_445', 
                '_446', '_447', '_448', '_449', '_450', 
                '_451', '_452', '_453', '_454', '_455', 
                '_456', '_457', '_458', '_459', '_460', 
                '_461', '_462', '_463', '_464', '_465', 
                '_466', '_467', '_468', '_469', '_470', 
                '_471', '_472', '_473', '_474', '_475', 
                '_476', '_477', '_478', '_479', '_480', 
                '_481', '_482', '_483', '_484', '_485', 
                '_486', '_487', '_488', '_489', '_490', 
                '_491', '_492', '_493', '_494', '_495', 
                '_496', '_497', '_498', '_499', '_500', 
                '_501', '_502', '_503', '_504', '_505', 
                '_506', '_507', '_508', '_509', '_510', 
                '_511', '_512', '_513', '_514', '_515', 
                '_516', '_517', '_518', '_519', '_520', 
                '_521', '_522', '_523', '_524', '_525', 
                '_526', '_527', '_528', '_529', '_530', 
                '_531', '_532', '_533', '_534', '_535', 
                '_536', '_537', '_538', '_539', '_540', 
                '_541', '_542', '_543', '_544', '_545', 
                '_546', '_547', '_548', '_549', '_550', 
                '_551', '_552', '_553', '_554', '_555', 
                '_556', '_557', '_558', '_559', '_560', 
                '_561', '_562', '_563', '_564', '_565', 
                '_566', '_567', '_568', '_569', '_570', 
                '_571', '_572', '_573', '_574', '_575', 
                '_576', '_577', '_578', '_579', '_580', 
                '_581', '_582', '_583', '_584', '_585', 
                '_586', '_587', '_588', '_589', '_590', 
                '_591', '_592', '_593', '_594', '_595', 
                '_596', '_597', '_598', '_599', '_600', 
                '_601', '_602', '_603', '_604', '_605', 
                '_606', '_607', '_608', '_609', '_610', 
                '_611', '_612', '_613', '_614', '_615', 
                '_616', '_617', '_618', '_619', '_620', 
                '_621', '_622', '_623', '_624', '_625', 
                '_626', '_627', '_628', '_629', '_630', 
                '_631', '_632', '_633', '_634', '_635', 
                '_636', '_637', '_638', '_639', '_640', 
                '_641', '_642', '_643', '_644', '_645', 
                '_646', '_647', '_648', '_649', '_650', 
                '_651', '_652', '_653', '_654', '_655', 
                '_656', '_657', '_658', '_659', '_660', 
                '_661', '_662', '_663', '_664', '_665', 
                '_666', '_667', '_668', '_669', '_670', 
                '_671', '_672', '_673', '_674', '_675', 
                '_676', '_677', '_678', '_679', '_680', 
                '_681', '_682', '_683', '_684', '_685', 
                '_686', '_687', '_688', '_689', '_690', 
                '_691', '_692', '_693', '_694', '_695', 
                '_696', '_697', '_698', '_699', '_700', 
                '_701', '_702', '_703', '_704', '_705', 
                '_706', '_707', '_708', '_709', '_710', 
                '_711', '_712', '_713', '_714', '_715', 
                '_716', '_717', '_718', '_719', '_720', 
                '_721', '_722', '_723', '_724', '_725', 
                '_726', '_727', '_728', '_729', '_730', 
                '_731', '_732', '_733', '_734', '_735', 
                '_736', '_737', '_738', '_739', '_740', 
                '_741', '_742', '_743', '_744', '_745', 
                '_746', '_747', '_748', '_749', '_750', 
                '_751', '_752', '_753', '_754', '_755', 
                '_756', '_757', '_758', '_759', '_760', 
                '_761', '_762', '_763', '_764', '_765', 
                '_766', '_767', '_768', '_769', '_770', 
                '_771', '_772', '_773', '_774', '_775', 
                '_776', '_777', '_778', '_779', '_780', 
                '_781', '_782', '_783', '_784', '_785', 
                '_786', '_787', '_788', '_789', '_790', 
                '_791', '_792', '_793', '_794', '_795', 
                '_796', '_797', '_798', '_799', '_800', 
                '_801', '_802', '_803', '_804', '_805', 
                '_806', '_807', '_808', '_809', '_810', 
                '_811', '_812', '_813', '_814', '_815', 
                '_816', '_817', '_818', '_819', '_820', 
                '_821', '_822', '_823', '_824', '_825', 
                '_826', '_827', '_828', '_829', '_830', 
                '_831', '_832', '_833', '_834', '_835', 
                '_836', '_837', '_838', '_839', '_840', 
                '_841', '_842', '_843', '_844', '_845', 
                '_846', '_847', '_848', '_849', '_850', 
                '_851', '_852', '_853', '_854', '_855', 
                '_856', '_857', '_858', '_859', '_860', 
                '_861', '_862', '_863', '_864', '_865', 
                '_866', '_867', '_868', '_869', '_870', 
                '_871', '_872', '_873', '_874', '_875', 
                '_876', '_877', '_878', '_879', '_880', 
                '_881', '_882', '_883', '_884', '_885', 
                '_886', '_887', '_888', '_889', '_890', 
                '_891', '_892', '_893', '_894', '_895', 
                '_896', '_897', '_898', '_899', '_900', 
                '_901', '_902', '_903', '_904', '_905', 
                '_906', '_907', '_908', '_909', '_910', 
                '_911', '_912', '_913', '_914', '_915', 
                '_916', '_917', '_918', '_919', '_920', 
                '_921', '_922', '_923', '_924', '_925', 
                '_926', '_927', '_928', '_929', '_930', 
                '_931', '_932', '_933', '_934', '_935', 
                '_936', '_937', '_938', '_939', '_940', 
                '_941', '_942', '_943', '_944', '_945', 
                '_946', '_947', '_948', '_949', '_950', 
                '_951', '_952', '_953', '_954', '_955', 
                '_956', '_957', '_958', '_959', '_960', 
                '_961', '_962', '_963', '_964', '_965', 
                '_966', '_967', '_968', '_969', '_970', 
                '_971', '_972', '_973', '_974', '_975', 
                '_976', '_977', '_978', '_979', '_980', 
                '_981', '_982', '_983', '_984', '_985', 
                '_986', '_987', '_988', '_989', '_990', 
                '_991', '_992', '_993', '_994', '_995', 
                '_996', '_997', '_998', '_999', '_1000', 
                '_1001', '_1002', '_1003', '_1004', '_1005', 
                '_1006', '_1007', '_1008', '_1009', '_1010', 
                '_1011', '_1012', '_1013', '_1014', '_1015', 
                '_1016', '_1017', '_1018', '_1019', '_1020', 
                '_1021', '_1022', '_1023', '_1024', '_1025', 
                '_1026', '_1027', '_1028', '_1029', '_1030', 
                '_1031', '_1032', '_1033', '_1034', '_1035', 
                '_1036', '_1037', '_1038', '_1039', '_1040', 
                '_1041', '_1042', '_1043', '_1044', '_1045', 
                '_1046', '_1047', '_1048', '_1049', '_1050', 
                '_1051', '_1052', '_1053', '_1054', '_1055', 
                '_1056', '_1057', '_1058', '_1059', '_1060', 
                '_1061', '_1062', '_1063', '_1064', '_1065', 
                '_1066', '_1067', '_1068', '_1069', '_1070', 
                '_1071', '_1072', '_1073', '_1074', '_1075', 
                '_1076', '_1077', '_1078', '_1079', '_1080', 
                '_1081', '_1082', '_1083', '_1084', '_1085', 
                '_1086', '_1087', '_1088', '_1089', '_1090', 
                '_1091', '_1092', '_1093', '_1094', '_1095', 
                '_1096', '_1097', '_1098', '_1099', '_1100', 
                '_1101', '_1102', '_1103', '_1104', '_1105', 
                '_1106', '_1107', '_1108', '_1109', '_1110', 
                '_1111', '_1112', '_1113', '_1114', '_1115', 
                '_1116', '_1117', '_1118', '_1119', '_1120', 
                '_1121', '_1122', '_1123', '_1124', '_1125', 
                '_1126', '_1127', '_1128', '_1129', '_1130', 
                '_1131', '_1132', '_1133', '_1134', '_1135', 
                '_1136', '_1137', '_1138', '_1139', '_1140', 
                '_1141', '_1142', '_1143', '_1144', '_1145', 
                '_1146', '_1147', '_1148', '_1149', '_1150', 
                '_1151', '_1152', '_1153', '_1154', '_1155', 
                '_1156', '_1157', '_1158', '_1159', '_1160', 
                '_1161', '_1162', '_1163', '_1164', '_1165', 
                '_1166', '_1167', '_1168', '_1169', '_1170', 
                '_1171', '_1172', '_1173', '_1174', '_1175', 
                '_1176', '_1177', '_1178', '_1179', '_1180', 
                '_1181', '_1182', '_1183', '_1184', '_1185', 
                '_1186', '_1187', '_1188', '_1189', '_1190', 
                '_1191', '_1192', '_1193', '_1194', '_1195', 
                '_1196', '_1197', '_1198', '_1199', '_1200', 
                '_1201', '_1202', '_1203', '_1204', '_1205', 
                '_1206', '_1207', '_1208', '_1209', '_1210', 
                '_1211', '_1212', '_1213', '_1214', '_1215', 
                '_1216', '_1217', '_1218', '_1219', '_1220', 
                '_1221', '_1222', '_1223', '_1224', '_1225', 
                '_1226', '_1227', '_1228', '_1229', '_1230', 
                '_1231', '_1232', '_1233', '_1234', '_1235', 
                '_1236', '_1237', '_1238', '_1239', '_1240', 
                '_1241', '_1242', '_1243', '_1244', '_1245', 
                '_1246', '_1247', '_1248', '_1249', '_1250', 
                '_1251', '_1252', '_1253', '_1254', '_1255', 
                '_1256', '_1257', '_1258', '_1259', '_1260', 
                '_1261', '_1262', '_1263', '_1264', '_1265', 
                '_1266', '_1267', '_1268', '_1269', '_1270', 
                '_1271', '_1272', '_1273', '_1274', '_1275', 
                '_1276', '_1277', '_1278', '_1279', '_1280', 
                '_1281', '_1282', '_1283', '_1284', '_1285', 
                '_1286', '_1287', '_1288', '_1289', '_1290', 
                '_1291', '_1292', '_1293', '_1294', '_1295', 
                '_1296', '_1297', '_1298', '_1299', '_1300', 
                '_1301', '_1302', '_1303', '_1304', '_1305', 
                '_1306', '_1307', '_1308', '_1309', '_1310', 
                '_1311', '_1312', '_1313', '_1314', '_1315', 
                '_1316', '_1317', '_1318', '_1319', '_1320', 
                '_1321', '_1322', '_1323', '_1324', '_1325', 
                '_1326', '_1327', '_1328', '_1329', '_1330', 
                '_1331', '_1332', '_1333', '_1334', '_1335', 
                '_1336', '_1337', '_1338', '_1339', '_1340', 
                '_1341', '_1342', '_1343', '_1344', '_1345', 
                '_1346', '_1347', '_1348', '_1349', '_1350', 
                '_1351', '_1352', '_1353', '_1354', '_1355', 
                '_1356', '_1357', '_1358', '_1359', '_1360', 
                '_1361', '_1362', '_1363', '_1364', '_1365', 
                '_1366', '_1367', '_1368', '_1369', '_1370', 
                '_1371', '_1372', '_1373', '_1374', '_1375', 
                '_1376', '_1377', '_1378', '_1379', '_1380', 
                '_1381', '_1382', '_1383', '_1384', '_1385', 
                '_1386', '_1387', '_1388', '_1389', '_1390', 
                '_1391', '_1392', '_1393', '_1394', '_1395', 
                '_1396', '_1397', '_1398', '_1399', '_1400', 
                '_1401', '_1402', '_1403', '_1404', '_1405', 
                '_1406', '_1407', '_1408', '_1409', '_1410', 
                '_1411', '_1412', '_1413', '_1414', '_1415', 
                '_1416', '_1417', '_1418', '_1419', '_1420', 
                '_1421', '_1422', '_1423', '_1424', '_1425', 
                '_1426', '_1427', '_1428', '_1429', '_1430', 
                '_1431', '_1432', '_1433', '_1434', '_1435', 
                '_1436', '_1437', '_1438', '_1439', '_1440', 
                '_1441', '_1442', '_1443', '_1444', '_1445', 
                '_1446', '_1447', '_1448', '_1449', '_1450', 
                '_1451', '_1452', '_1453', '_1454', '_1455', 
                '_1456', '_1457', '_1458', '_1459', '_1460', 
                '_1461', '_1462', '_1463', '_1464', '_1465', 
                '_1466', '_1467', '_1468', '_1469', '_1470', 
                '_1471', '_1472', '_1473', '_1474', '_1475', 
                '_1476', '_1477', '_1478', '_1479', '_1480', 
                '_1481', '_1482', '_1483', '_1484', '_1485', 
                '_1486', '_1487', '_1488', '_1489', '_1490', 
                '_1491', '_1492', '_1493', '_1494', '_1495', 
                '_1496', '_1497', '_1498', '_1499', '_1500', 
                '_1501', '_1502', '_1503', '_1504', '_1505', 
                '_1506', '_1507', '_1508', '_1509', '_1510', 
                '_1511', '_1512', '_1513', '_1514', '_1515', 
                '_1516', '_1517', '_1518', '_1519', '_1520', 
                '_1521', '_1522', '_1523', '_1524', '_1525', 
                '_1526', '_1527', '_1528', '_1529', '_1530', 
                '_1531', '_1532', '_1533', '_1534', '_1535', 
                '_1536', '_1537', '_1538', '_1539', '_1540', 
                '_1541', '_1542', '_1543', '_1544', '_1545', 
                '_1546', '_1547', '_1548', '_1549', '_1550', 
                '_1551', '_1552', '_1553', '_1554', '_1555', 
                '_1556', '_1557', '_1558', '_1559', '_1560', 
                '_1561', '_1562', '_1563', '_1564', '_1565', 
                '_1566', '_1567', '_1568', '_1569', '_1570', 
                '_1571', '_1572', '_1573', '_1574', '_1575', 
                '_1576', '_1577', '_1578', '_1579', '_1580', 
                '_1581', '_1582', '_1583', '_1584', '_1585', 
                '_1586', '_1587', '_1588', '_1589', '_1590', 
                '_1591', '_1592', '_1593', '_1594', '_1595', 
                '_1596', '_1597', '_1598', '_1599')
# CLASSES = ('__background__', # always index 0
#                   '_1' , '_2' , '_3' , '_4' ,
#                   '_5' , '_6' , '_7' , '_8' , '_9',
#                   '_10', '_11', '_12', '_13', '_14',
#                   '_15', '_16', '_17', '_18', '_19',
#                   '_20', '_21', '_22', '_23', '_24',
#                   '_25', '_26', '_27', '_28', '_29',
#                   '_30', '_31', '_32', '_33', '_34',
#                   '_35', '_36', '_37', '_38', '_39',
#                   '_40', '_41', '_42', '_43', '_44',
#                   '_45', '_46', '_47', '_48', '_49',
#                   '_50', '_51', '_52', '_53', '_54',
#                   '_55', '_56', '_57', '_58', '_59',
#                   '_60', '_61', '_62', '_63', '_64',
#                   '_65', '_66', '_67', '_68', '_69',
#                   '_70', '_71', '_72', '_73', '_74',
#                   '_75', '_76', '_77', '_78', '_79',
#                   '_80', '_81', '_82', '_83', '_84',
#                   '_85', '_86', '_87', '_88', '_89',
#                   '_90', '_91', '_92', '_93', '_94',
#                   '_95', '_96', '_97', '_98', '_99',
#                   '_100')


NETS = {'vgg16': ('VGG16',
                  'VGG16_faster_rcnn_final.caffemodel'),
        'zf': ('ZF',
                  'ZF_faster_rcnn_final.caffemodel'),
        'APC': ('APC',
            'vgg_cnn_m_1024_faster_rcnn_iter_70000seed_3_book.caffemodel'),
            # 'vgg_cnn_m_1024_faster_rcnn_iter_70000seed_3_sippy_cup_pose_estimation.caffemodel'),
                  # 'vgg_cnn_m_1024_faster_rcnn_iter_70000seed_3_classificationBottle.caffemodel'),
        #'674':('674',
         #         'vgg_cnn_m_1024_faster_rcnn_iter_70000seed_3.caffemodel')}        
        '674':('674',
                  'vgg16_faster_rcnn_iter_60000seed_3.caffemodel')}


def vis_detections(im, im_file, class_name, dets, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return

    im = im[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(im, aspect='equal')
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]

        ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1], fill=False,
                          edgecolor='red', linewidth=3.5)
            )
        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(class_name, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')

    ax.set_title(('{} detections with '
                  'p({} | box) >= {:.1f} {}').format(class_name, class_name,
                                                  thresh, im_file),
                  fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.draw()
    plt.show()
    return int(class_name)

def demo(net):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image

    #im_file = os.path.join(cfg.DATA_DIR, 'demo', image_name)
    #folder = 'real_test'
    folder = 'real_test_25'
    #folder = 'book_pose_test_virtual'
    
    # (1) virtual images
    ftest = open(os.path.join('/home/zhusj/Github/py-faster-rcnn/data/APC/',folder, 'Imagelist.txt'),'r')
    outputFile = open(os.path.join('/home/zhusj/Github/py-faster-rcnn/data/APC/',folder, 'result.txt'),'w')
   
    number = ftest.readline().strip()

    bbox_filename = os.path.join('/home/zhusj/Github/py-faster-rcnn/data/APC/', folder,'bbox_'+number+'.txt')
    while bbox_filename:
        with open(bbox_filename, "r") as filestream:
            print bbox_filename
            im_file = os.path.join('/home/zhusj/Github/py-faster-rcnn/data/APC/', folder, 'image_'+number+'.png')
            # print im_file
            im = cv2.imread(im_file)

            # Detect all object classes and regress object bounds
            timer = Timer()
            timer.tic()
            scores, boxes = im_detect(net, im)
            timer.toc()
            print ('Detection took {:.3f}s for '
                   '{:d} object proposals').format(timer.total_time, boxes.shape[0])
            for i in range(1, 1600):
                #currentline = line.split(",")

                CONF_THRESH = 0.05
                NMS_THRESH = 0.05
                result = np.zeros(12)

                # print currentline
                cls_ind = i
                cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
                cls_scores = scores[:, cls_ind]
                dets = np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
                keep = nms(dets, NMS_THRESH)
                dets = dets[keep, :]
                inds = np.where(dets[:, -1] >= CONF_THRESH)[0]
                # if inds.shape[0]>0:
                # if inds.any:
                print "inds:", inds
                id = vis_detections(im, im_file, str(cls_ind), dets, thresh=CONF_THRESH)
                # print "dets:", dets
                # print "cls_boxes:", cls_boxes
                bbox = dets[0, :4]
                if len(inds) > 0:
                    outputFile2 = open(os.path.join('/home/zhusj/Github/py-faster-rcnn/data/APC/', folder, 'boxes_'+number+'.txt'),'w')
                    outputFile2.write(str(number)+','+str(int(bbox[0]))+','+ str(int(bbox[1]))+','+ str(int(bbox[2]))+','+ str(int(bbox[3])))
                outputFile.write(str(number)+','+str(i)+','+str(int(bbox[0]))+','+ str(int(bbox[1]))+','+ str(int(bbox[2]))+','+ str(int(bbox[3])))
                outputFile.write('\n')
                # else:
                #     # cls_scores_sorted = sorted(cls_scores)
                #     sort_index = np.argsort(cls_scores)
                #     # print  cls_scores_sorted[0],cls_scores_sorted[-1]
                #     print  cls_scores[sort_index[0]],cls_scores[sort_index[-1]]
                #     bbox = cls_boxes[sort_index[-1], :4]
                #     outputFile.write(currentline[0]+','+str(int(bbox[0]))+','+ str(int(bbox[1]))+','+ str(int(bbox[2]))+','+ str(int(bbox[3])))
                #     outputFile.write('\n')
                # else:
                #     outputFile.write(currentline[0]+','+str(280)+','+ str(160)+','+ str(360)+','+ str(240))
                #     outputFile.write('\n')

            # print number        
            number = ftest.readline().strip() 
            if number:            
                bbox_filename = os.path.join('/home/zhusj/Github/py-faster-rcnn/data/APC/', folder,'bbox_'+number+'.txt')
            else:
                break
           
    #id = vis_detections(im, cls, dets, thresh=CONF_THRESH)
    # if id:
    #     result[id-1]=1

    # return result, dets

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Faster R-CNN demo')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]',
                        default=0, type=int)
    parser.add_argument('--cpu', dest='cpu_mode',
                        help='Use CPU mode (overrides --gpu)',
                        action='store_true')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16]',
                        choices=NETS.keys(), default='vgg16')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    args = parse_args()


    #prototxt = os.path.join(cfg.MODELS_DIR, NETS[args.demo_net][0],
    #                        'faster_rcnn_alt_opt', 'faster_rcnn_test.pt')
    caffemodel = os.path.join(cfg.DATA_DIR, 'faster_rcnn_models',
                              NETS[args.demo_net][1])

    prototxt = '/home/zhusj/Github/py-faster-rcnn/models/APC/VGG_CNN_M_1024/faster_rcnn_end2end/test.prototxt'
    #caffemodel = '/home/zhusj/Github/py-faster-rcnn/output/foobar/CS674/vgg_cnn_m_1024_faster_rcnn_iter_20000seed_3.caffemodel'
    if not os.path.isfile(caffemodel):
        raise IOError(('{:s} not found.').format(caffemodel))
    if not os.path.isfile(prototxt):
        raise IOError(('{:s} not found.').format(prototxt))

    if args.cpu_mode:
        caffe.set_mode_cpu()
    else:
        caffe.set_mode_gpu()
        caffe.set_device(args.gpu_id)
        cfg.GPU_ID = args.gpu_id
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)

    print '\n\nLoaded network {:s}'.format(caffemodel)

    # Warmup on a dummy image
    im = 128 * np.ones((300, 500, 3), dtype=np.uint8)
    for i in xrange(2):
        _, _= im_detect(net, im)

 #   im_names = ['000456.jpg', '000542.jpg', '001150.jpg',
  #              '001763.jpg', '004545.jpg']
  #  im_names = ['image_972.png']

  #  for im_name in im_names:
  #      print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
  #      print 'Demo for data/demo/{}'.format(im_name)
  #      demo(net, im_name)

  #  plt.show()
    # ftest = open('recognition_imageList.txt','r')
    # outputFile = open('RecognitionResult.txt','w')
    # number = ftest.readline().strip()
    # im_name = '/home/zhusj/Github/py-faster-rcnn/data/CS674/Recognition/test1/'+'image_'+number+'.png'
    # # result = demo(net, im_name)
    # # for x in xrange(1,13):
    # #     outputFile.write(str(number)+'_'+str(int(x))+','+str(int(result[x-1])))
    # #     outputFile.write('\n')
    # # print result
    # #plt.show()
    # #cv2.waitKey(0)
    # while im_name:
    #     print im_name
    #     result, dets = demo(net, im_name)

    #     for x in xrange(1,13):
    #         outputFile.write(str(number)+'_'+str(int(x))+','+str(int(result[x-1])))
    #         outputFile.write('\n')
    #     #plt.show()
    #     #cv2.waitKey(0)
    #     number = ftest.readline().strip() 
    #     if number:            
    #         im_name = '/home/zhusj/Github/py-faster-rcnn/data/CS674/Recognition/test1/'+'image_'+number+'.png'
    #     else:
    #         break

    #plt.show()
    demo(net)