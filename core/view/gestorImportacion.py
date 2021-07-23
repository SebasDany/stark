
from time import perf_counter
from django.shortcuts import render, redirect

from ..controlador import  buscarSKU, saveDetalleImportacion,saveMercacia ,saveProducto, saveDetalleImportacion
from ..ecommerce import Woocommerce

from django.shortcuts import render, redirect
from django.utils.html import escape
from ..models import Mercancia,Producto,Detalle_afianzado,Detalle_das, Detalle_importacion,Das,Factura_afianzado,Factura_proveedor,Importacion,Afianzado,Proveedor,Proveedor_producto
from django.http import HttpResponse
from woocommerce import API
from ..forms import UserRegisterForm, ProductRegister, FormImportacion, FormDas,FormFacturaProveedor,FormFacturaAfianzado,FormDetalleAfianzado


from django.contrib import messages
import json
import datetime

# wcapi = API(
#             url="https://avelectronics.cc",  # Your store URL
#             consumer_key="ck_e0f2084ef185f4caa1c35bc2df6faeb53adf2311",  # Your consumer key
#             consumer_secret="cs_7028c29153ab8a43383d84a777c91d4cd9df4d2e",  # Your consumer secret
#             wp_api=True,  # Enable the WP REST API integration
#             version="wc/v3"  # WooCommerce WP REST API version
#         )

# products =wcapi.get("products")
# print(products.status_code)
# productos=products.json()
# print(productos[0].get('sku'))
sku=['AA001', 'AA002', 'AA003', 'AC001', 'AC002', 'AC003', 'AC004', 'AC009', 'AG001', 'AG002', 'AO001', 'AG003', 'AG004', 'AG005', 'AG006', 'AG007', 'AG008', 'AG009', 'AG013', 'AG014', 'AG010', 'AG011', 'AG016', 'AG017', 'AG015', 'AO002', 'AO003', 'AO005', 'AO004', 'AO008', 'AO006', 'AO007', 'AS023', 'AS001', 'AS003', 'AS005', 'AS006', 'AS008', 'AS009', 'AS010', 'AS011', 'AS013', 'AS014', 'AS015', 'AS016', 'AS017', 'AS018', 'AS019', 'AS020', 'AS022', 'AS025', 'ME001', 'AS026', 'AS027', 'CO001', 'CO003', 'CO002', 'CO013', 'CO004', 'CO005', 'CO006', 'CO007', 'CO008', 'CO009', 'CO010', 'CO011', 'CO012', 'CO015', 'MA001', 'MA002', 'MD001', 'MD002', 'MD003', 'MD006', 'MD005', 'AU002', 'ME003', 'ME004', 'ME005', 'ME006', 'ME007', 'MI008', 'MI009', 'MI010', 'MI011', 'MI012', 'AC020', 'AC021', 'AC019', 'AC018', 'AC016', 'AC017', 'MI022', 'MI023', 'MI024', 'MI025', 'RR004', 'AC014', 'MO001', 'MO002', 'MO003', 'MO004', 'MO007', 'MO008', 'MO009', 'P1086', 'P1087', 'P1088', 'P1089', 'P1093', 'P1101', 'P1127', 'P1132', 'P1134', 'P1220', 'P1300', 'P1356', 'P1415', 'P1416', 'P1418', 'P1419', 'P1420', 'P1424', 'P1425', 'P1429', 'P1645', 'P2118', 'P2123', 'P2130', 'P2361', 'P2456', 'P2457', 'P2458', 'P2459', 'P2465', 'P2510', 'P2570', 'P2850', 'P2851', 'P3061', 'P3063', 'P3065', 'P3101', 'P3125', 'P3062', 'P713', 'P951', 'P960', 'P961', 'P975', 'P998', 'P999', 'PA001', 'PA002', 'PA003', 'PA004', 'PA005', 'PA006', 'PA007', 'PR001', 'PR002', 'PR003', 'RA001', 'RA002', 'RA003', 'RA004', 'RA005', 'RA006', 'RA007', 'RA009', 'RK003', 'RK005', 'RK006', 'RN001', 'RN002', 'RN003', 'RP002', 'RA017', 'RP003', 'RR001', 'RR002', 'RR003', 'SE001', 'SE002', 'SE003', 'SE004', 'SE005', 'SE006', 'SE007', 'SE008', 'SE009', 'SE010', 'SE011', 'SE012', 'SE013', 'SE014', 'SE015', 'SE016', 'SE017', 'SE018', 'SE019', 'SE021', 'SE022', 'SE023', 'SE024', 'SE026', 'SE027', 'SE028', 'SE029', 'SE030', 'SE033', 'SE038', 'SE032', 'P1696', 'SE036', 'AC015', 'MD004', 'SE037', 'CH001', 'PA008', 'RE001', 'P3126', 'P3073', 'P3074', 'P798', 'P3575', 'RP001', 'RP004', 'CO016', 'CO017', 'AS028', 'AS029', 'SE025', 'SE020', 'SE031', 'AC010', 'AC011', 'AC012', 'AC013', 'CO014', 'P1430', 'P3081', 'P2990', 'SE034', 'CO018', 'AS007', 'SE041', 'RE002', 'SE039', 'SE040', 'RR005', 'RP004-1', 'PA009-1', 'P2450', 'P3030', 'P1454', 'P1452', 'P3170', 'P3214', 'P3215', 'P3039', 'B11901', 'B09275', 'B10280', 'B09181', 'B08935', 'B09187', 'B18205', 'B11897', 'CH7637', 'B88962', 'B11900', 'B26452', 'B23821', 'B22906', 'SE042', 'CO019', 'FE001', 'FE002', 'NX001', 'NX002', 'PA010', 'NX004', 'NX003', 'P3071', 'P642', 'P3080', 'P2590', 'SE043', 'SE044', 'PR004', 'MI003', 'MI004', 'SE045', 'SE046', 'SE047', 'SE048', 'SE049', 'SE050', 'AG012', 'AC005', 'MO010', 'SE051', 'SE052', 'SE053', 'AC022', 'CO020', 'PR005', 'MO011', 'MO012', 'MO013', 'MO014', 'MO015', 'MO016', 'MO017', 'MO018', 'MO019', 'MO020', 'MA003', 'RA008', 'RA010', 'CH005', 'CH21044', 'B110537', 'B26738', 'B41271', 'B20386', 'B9964', 'B64210', 'B9273', 'B88955', 'MD007', 'MD008', 'AU001', 'MI001', 'MD009', 'AS030', 'AS031', 'RP001-1', 'P799', 'P1572', 'P1573', 'P3203', 'P3202', 'P3075', 'P950', 'P953', 'FT001', 'FT002', 'FT003', 'FT004', 'FT005', 'FT021', 'FT023', 'FT022', 'FT030', 'FT031', 'FT052', 'FT051', 'FT071', 'FT072', 'FT006', 'AG019', 'AG020', 'SE054', 'SE055', 'SE056', 'MI002', 'MO005', 'CO021', 'SE057', 'ME008', 'ME009', 'ME010', 'MD010', 'MI005', 'MI006', 'MI007', 'MO021', 'MD011', 'SE058', 'AS032', 'AS033', 'CO022', 'CID001', 'CID002', 'SE059', 'MI027', 'MI026', 'RE003', 'RE004', 'EP001', 'EP003', 'EP003-10', 'EP003-22', 'EP003-47', 'EP003-100', 'EP003-150', 'EP003-200', 'EP003-220', 'EP003-270', 'EP003-330', 'EP003-470', 'EP003-510', 'EP003-680', 'EP003-1k', 'EP003-2.2k', 'EP003-3.3k', 'EP003-4.7k', 'EP003-5.1k', 'EP003-6.8k', 'EP003-10k', 'EP003-20k', 'EP003-47k', 'EP003-51k', 'EP003-68k', 'EP003-100k', 'EP003-220k', 'EP003-300k', 'EP003-470k', 'EP003-680k', 'EP003-1m', 'CO023', 'CT001', 'CT002', 'MO022', 'SE060', 'CH004', 'SE061', 'SE062', 'AU003', 'MD012', 'CH002', 'RK004', 'BT001', 'SE063', 'ME002', 'RK007', 'MA004', 'MA005', 'EP004', 'EP004-1k', 'EP004-1m', 'EP004-10k', 'EP004-10', 'EP004-100k', 'EP004-100', 'EP004-1.5k', 'EP004-2.2k', 'EP004-15k', 'EP004-22', 'EP004-10m', 'EP004-220', 'EP004-3.3k', 'EP004-330k', 'EP004-330', 'EP004-5.6k', 'EP004-47k', 'EP004-47', 'EP004-470k', 'EP004-470', 'EP004-4.7k', 'EP004-56k', 'EP004-560', 'EP004-6.8k', 'EP004-68k', 'EP004-680k', 'EP004-680', 'EP004-1', 'EP004-22k', 'EP004-33k', 'EP005', 'EP005-1', 'EP005-10', 'EP005-22', 'EP005-47', 'EP005-100', 'EP005-220', 'EP005-330', 'EP005-470', 'EP005-560', 'EP005-680', 'EP005-1k', 'EP005-1.5k', 'EP005-2.2k', 'EP005-3.3k', 'EP005-4.7k', 'EP005-5.6k', 'EP005-6.8k', 'EP005-10k', 'EP005-15k', 'EP005-22k', 'EP005-33k', 'EP005-47k', 'EP005-56k', 'EP005-68k', 'EP005-100k', 'EP005-330k', 'EP005-470k', 'EP005-680k', 'EP005-1m', 'EP005-10m', 'EP006', 'EP007', 'EP006-1', 'EP006-2', 'EP006-3', 'EP006-4', 'EP006-5', 'EP006-6', 'EP006-7', 'EP006-9', 'EP006-8', 'EP007-1', 'EP007-2', 'EP007-3', 'EP007-4', 'EP007-5', 'EP007-6', 'EP007-7', 'FE003', 'EA001', 'EA001-1', 'EA002', 'EA002-1', 'EA002-2', 'EA002-3', 'EA003', 'EA003-5', 'EA003-4', 'EA004', 'EA004-1', 'EA004-2', 'EA005', 'EA005-1', 'EA005-2', 'EA005-3', 'EA005-4', 'EA005-5', 'EA006', 'EA006-1', 'EA006-2', 'EA006-3', 'EA006-4', 'EA007', 'EA007-2', 'EA007-3', 'EA007-4', 'EA007-5', 'EA007-6', 'EA007-1', 'EA008', 'EA009', 'EP008', 'EP008-100k', 'EP008-50k', 'EP008-10k', 'EP008-5k', 'EP008-1k', 'EP009', 'EP009-100k', 'EP009-10k', 'EP009-1k', 'EP009-100', 'MO023', 'MI028', 'EA010', 'EA010-1', 'EA010-2', 'EP010', 'EP010-1', 'EP010-2', 'uC001', 'EP011', 'EP011-1', 'EP011-2', 'EP012', 'EP012-1', 'EP012-2', 'EP013', 'EP013-1', 'EP013-2', 'EP014', 'EP014-1', 'EP014-2', 'EP015', 'EP016', 'ME011', 'RE005', 'SE064', 'AC023', 'AC024', 'AC025', 'CI7400', 'CI7402', 'FE010', 'FE011', 'SE065', 'SE066', 'SE067', 'PA011', 'PA011-1', 'PA011-2', 'MI013', 'CO024', 'RE006', 'SE068', 'AK001', 'CO025', 'CO026', 'CI7404', 'CI7408', 'CI7411', 'CI7421', 'CI7427', 'CI7432', 'CI7447', 'CI7448', 'CI7473', 'CI7474', 'CI7485', 'CI7483', 'CI7486', 'CI7493', 'CI74107', 'CI74139', 'CI74153', 'CI74157', 'CI74192', 'CI4013', 'CI4015', 'CI4027', 'CI4029', 'CI4042', 'CI4052', 'CI40106', 'CI003', 'CI004', 'CI005', 'CI006', 'CI007', 'CI008', 'CI009', 'CI010', 'CI011', 'SE069', 'SE037-1', 'CH006', 'AG021', 'AG022', 'P989', 'P1695', 'P791', 'P2507', 'P2096', 'B9490', 'B178009', 'P2117', 'P4101', 'P4201', 'P4401', 'P4301', 'P4501', 'P4601', 'CO027', 'SE070', 'SE071', 'CO028', 'AU004', 'AU005', 'SE072', 'SE073', 'SE074', 'CO029', 'AG023', 'AG024', 'FE004', 'FE005', 'AK004', 'AK005', 'RK008', 'AK003', 'AK006', 'P3072', 'P3239', 'FT008', 'FT007', 'AC026', 'CI012', 'SE075', 'uC002', 'MI030', 'SE076', 'MD013', 'AS024', 'AS004', 'NX005', 'ST001', 'ST002', 'ST003', 'ST004', 'B26739', 'P1000', 'P3060', 'P3172', 'P3064', 'MO025', 'CO030', 'FE006', 'MI031', 'EP017', 'EP018', 'MO024', 'AU006', 'MI029', 'RA012', 'AVE001', 'AS034', 'RA013', 'RA014', 'NX006', 'RK009', 'MO026', 'MI014', 'MI015', 'MI016', 'ST005', 'ST006', 'ST007', 'RP005', 'RA015', 'RA016', 'RA018', 'NV001', 'CO031', 'MI032', 'MI032-1', 'MI032-2', 'MI032-3', 'MI033', 'MI033-1', 'MI033-2', 'MI033-3', 'MI034', 'P2999', 'P2997', 'P2520', 'RP006', 'RP007', 'P4843', 'P3037', 'EA003-3', 'EA003-1', 'EA003-2', 'EA004-4', 'EA004-3', 'EA013', 'EA013-2', 'EA013-1', 'EA014', 'EA014-2', 'EA014-1', 'EA012', 'EA012-3', 'EA012-2', 'EA012-1', 'uC006', 'uC004', 'uC005', 'uC009', 'uC007', 'uC008', 'uC003', 'EP004-2.7k', 'EP004-150k', 'EP004-510k', 'EP004-2.2m', 'EP004-4.7m', 'EP006-10', 'EP020', 'EP020-1', 'EP020-2', 'EP020-3', 'EP020-4', 'EP019', 'EP019-1', 'EP019-2', 'EP002', 'EP002-1', 'EP002-2', 'EP002-3', 'EP002-4', 'EP002-5', 'EP008-20k', 'EP021', 'EP021-6', 'EP021-7', 'EP021-8', 'EP021-9', 'EP021-10', 'EP021-5', 'EP021-4', 'EP021-3', 'EP021-2', 'EP021-1', 'EP010-4', 'EP010-3', 'CI002', 'MI035', 'MI035-2', 'MI035-3', 'MI035-4', 'MI036', 'MI036-2', 'MI036-3', 'MI036-4', 'MI036-1', 'MI040', 'EP022', 'EP022-1', 'EP022-2', 'EP023', 'EP024', 'EP014-3', 'EP014-4', 'EP030', 'AC027', 'MI041', 'HE012', 'HE013', 'MI044', 'MI045', 'MI046', 'MI046-2', 'MI046-1', 'HE010', 'MI037', 'EP031', 'EP031-1', 'EP031-2', 'MI049', 'MI050', 'HE003', 'CH010', 'CH011', 'HE001', 'HE002', 'HE005', 'HE006', 'HE008', 'PI001', 'PI002', 'PI003', 'PI004', 'PI005', 'MI039', 'SE077', 'MI062', 'MI038', 'MI048', 'MI048-1', 'MI051', 'MI051-1', 'MI051-2', 'CI013', 'CI014', 'CI015', 'CI016', 'EA011', 'EA011-1', 'EA011-2', 'MI053', 'MI053-6', 'MI053-7', 'MI053-5', 'MI053-4', 'MI053-3', 'MI053-2', 'MI053-1', 'MI055', 'MI055-2', 'MI055-1', 'MI056', 'MI057', 'EP025', 'EP025-3', 'EP025-2', 'EP025-1', 'EP026', 'MI058', 'MI059', 'MI060', 'MI061', 'MI061-4', 'MI061-3', 'MI061-2', 'MI063', 'EP032', 'EP032-1', 'EP032-2', 'EP033', 'EP034', 'HE014', 'MI064', 'MI046-3', 'EA015', 'EP005-560k', 'EP005-820', 'EP005-8.2k', 'EP005-82k', 'EP005-820k', 'MI053-8', 'RA019', 'RA020', 'ST008', 'MI065', 'HE015', 'HE016', 'HE017', 'HE018', 'SE078', 'SE079', 'PA012', 'MD014', 'SE080', 'HE020', 'RE007', 'FE012', 'SE082', 'RK002', 'SE081', 'HE021', 'HE022', 'CO032', 'MI066', 'RE008', 'SE083', 'SE084', 'AC028', 'EP019-3', 'EP035', 'EP035-4', 'EP035-5', 'EP035-3', 'EP035-2', 'EP035-1', 'MI063-1', 'MI063-2', 'MI062-1', 'MI062-2', 'MI046-5', 'MI046-4', 'HE023', 'HE024', 'HE025', 'HE025-1', 'HE025-2', 'HE026', 'EP008-500k', 'EA003-6', 'EA016-1', 'EA016-2', 'AA004', 'SE085', 'SE056-2', 'MI017', 'MI036-5', 'MI036-6', 'MI036-7',]


wcapi1 = API(
        url="http://18.217.125.242/", # Your store URL
        consumer_key="ck_d27e19bf8855d4c1e8a0e7dc3d652fa8cdb27643", # Your consumer key
        consumer_secret="cs_8e1544fe175c35d1af7b9f30fe5a03f185be5497", # Your consumer secret
        wp_api=True, # Enable the WP REST API integration
        version="wc/v3" # WooCommerce WP REST API version
    )

mercancia=['TARJETAS ELECTRÓNICAS', 'SENSORES', 'SENSORES MEDIDOR D', 'Carcasa De Plastico', 'Sensor De Microfono', 'PARTE DE CAMARA', 'Mini Pantalla Display', 'RELE', 'CABLES', 'REGULADORES DE VOLTAJE', 'RECEPTOR INALAMBRICO', 'KIT DE ROBOTICA', 'CIRCUITOS INTEGRADOS', 'PORTA LED', 'DIODOS', 'SOPORTE PARA TARJETAS', 'INTERRUPTORES', 'RESISTENCIAS',]
subpartida=['8542390000','9031809000','9025900000','3926909000','8518909090','9006910000','8531200000','8536419000','8544429000','9032891100','8517692000','8543709000','8542310000','8541900000','8541100000','8542900000','8536690090','8533319000']
por_advalorem=[0, 0, 0, 0.29, 0.9, 2.38, 0, 0.32, 4.15, 1.67, 3.24, 0, 0, 0, 0, 0, 1.2, 0,]
#saveMercacia(mercancia,subpartida,por_advalorem) #gurada la mercancia

sku=['AA001', 'AA002', 'AA003', 'AC001', 'AC002', 'AC003', 'AC004', 'AC009', 'AG001', 'AG002',
     'AO001', 'AG003', 'AG004', 'AG005', 'AG006', 'AG007', 'AG008', 'AG009', 'AG013', 'AG014',
     'AG010', 'AG011', 'AG016', 'AG017', 'AG015', 'AO002', 'AO003', 'AO005', 'AO004', 'AO008', 
     'AO006', 'AO007', 'AS023', 'AS001', 'AS003', 'AS005', 'AS006', 'AS008', 'AS009', 'AS010', 
     'AS011', 'AS013', 'AS014', 'AS015', 'AS016', 'AS017', 'AS018', 'AS019', 'AS020', 'AS022', 
     'AS025', 'ME001', 'AS026', 'AS027', 'CO001', 'CO003', 'CO002', 'CO013', 'CO004', 'CO005', 
     'CO006', 'CO007', 'CO008', 'CO009', 'CO010', 'CO011', 'CO012', 'CO015', 'MA001', 'MA002', 
     'MD001', 'MD002', 'MD003', 'MD006', 'MD005', 'AU002', 'ME003', 'ME004', 'ME005', 'ME006', 
     'ME007', 'MI008', 'MI009', 'MI010', 'MI011', 'MI012', 'AC020', 'AC021', 'AC019', 'AC018', 
     'AC016']
nombre=["NFC NTAG®215 Round White Sticker",
"TI DIP 0,1USD/PCS   ",
"TI  DIP 0,1USD/PCS   ",
"TI  DIP 0,12USD/PCS   ",
"TI DIP 0,12USD/PCS  ",
"TI  DIP 0,12USD/PCS   ",
"TI DIP 0,16USD/PCS   ",
"BUZZER 12*9,5  0,1USD/PCS   ",
"Zocalo base DIP CI 18 pin ",
"Zocalo base DIP CI 20 pin ",
"Zocalo base DIP CI  28 pin  ",
"Zocalo base DIP CI 40 pin  ",
"2N2222A ST TO92   ",
" BC547C NXP  T092 ",
"MAX485CPA  MAXIM  DIP ",
"MCP3208-CI/SL  MICROCHIP ",
" LM741CN TI   DIP8 0,36USD/PCS  200PCS  ",
"TL082CN  ST DIP  0,37USD/PCS    ",
"Resistencias carbón 1/4W 1K   ",
"Resistencias carbón 1/4W 10K    ",
"Resistencias carbón 1/4W 100K  ",
"Resistencias metálica 1/4W 10K ",
"BTA16-600BWRG   ST  TO220  17+  ",
"BTA12-600CRG   ST  TO220 ",
"BT131-600   NXP  TO-92",
"SN7448N TI DIP 0,22USD/PCS   ",
"SN7411N  TI  DIP  13+  0,4USD/EA   ",
"SN7421N TI DIP  0,   ",
"SN7483N TI DIP  0,62USD/PCS    ",
"SN7410N TI DIP  0,46USD/PCS   ",
"SN7420N TI DIP 0,4USD/PCS    ",
"SN7427N  TI DIP 0,35USD/PCS    ",
"SN7425N TI DIP 0,83USD/PCS  ",
"SN74373N TI DIP 0,54USD/PCS ",
" CD4008BE DIP16 0,55USD/PCS   ",
"CD4063BE TI DIP 0,18USD/PCS   ",
"led holder 5mm 0,015USD/PCS  ",
"5MM RGB LED  Ánodo Común  0,03USD/PCS  500PCS  ",
"5MM RGB LED  Cátodo Común 0,03USD/PCS  500PCS  ",
"L7805CV ST TO220  0,08USD/PCS 500PCS  ",
"M3*11+6 mm male-female  0,05USD/PCS   ",
"M3*15+6mm male-female 0,06USD/PCS ",
"M3*20+6mm  male-female 0,062USD/PCS    ",
"0,39INCH 4digital  ",
"LM35DZ  TI  TO92  0,54USD/PCS  ",
"PIC16F628A-I/P  ",
"3-pin DPDT toggle switch 0, ",
"TIP120 FAIRCHILD  TO-220 0,456USD/PCS   ",
" TIP32C   ST  TO220  0,157USD/PCS    ",
"TIP31C    ST TO220 0,18USD/PCS    ",
" ULN2803APG TOSHIBA  DIP  ",
"MOC3020M  FSC  DIP 0,128USD/PCS    ",
"4N35M FSC DIP  0,11USD/PCS   ",
"L293D ST DIP 1,32USD/PCS     ",
"MEGA 2560 R3 with arduino logo",
"UNO R3 with arduino logo ",
"Digital Sound Sensor",
"Pro mini 5V/16MHz",
"W1209 Digital thermostat with ",
"acrylic case for UNO R3",
"Microphone sensor k",
"MQ-2 Sensor",
"TTP223B touch sensor",
"CSI interface camera ",
"Infrared Obstacle Avoidance Module Arduino",
"ADS1115 16ch Digital Analog Converter",
"RTC DS1302 (with battery) without battery",
"RTC DS1307 without battery",
"13,56mhz IC tag",
"LDR Light Sensor Module",
"0,96 White I2C IIC",
"2 Channel Relay Module 5V",
"ST LINK Stlink ST-Link ",
"Dupont Cable Female – Male 10cm 40pcs",
"Dupont Cable Female – Female 10cm 40pcs",
"Dupont Cable Male – Male 10cm 40pcs",
"Dupont Cable Male – Male 20cm 40pcs",
"Dupont Cable Female – Male 20cm 40pcs",
"Dupont Cable Female – Female 20cm 40pcs",
"3S 12V 18650 10A BMS ",
"5x7cm DIY Prototype T",
"Raspberry pi 3 model",
"Raspberry Pi Pi2 5 ",
"7 inch Raspberry ",
"XL6009 4A 3V-32V ",
"2262/2272 315Mhz ",
"Nano V3,0 ATMEGA328P   cable",
"MEGA 2560 R3 CH340 WITH 30cm USB CABLE",
"Motor Smart Robot Car Chassis ",
"2,8 TFT 320x240 NX3224T028 HMI Resistive",
"315MHz RF 4 Channel Remote Control EV1527"
]
id_w=[]
id_w.append(1)
precio_compra=[]
precio_neto=[]
variacion =[]
parent_id=[]
imagen=[]
categorias=[]
observaciones=[]
mercan=["TARJETAS ELECTRÓNICAS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "TARJETAS ELECTRÓNICAS", "SOPORTE PARA TARJETAS", "SOPORTE PARA TARJETAS", "SOPORTE PARA TARJETAS", "SOPORTE PARA TARJETAS", "DIODOS", "DIODOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "RESISTENCIAS", "RESISTENCIAS", "RESISTENCIAS", "RESISTENCIAS", "DIODOS", "DIODOS", "DIODOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "PORTA LED", "DIODOS", "DIODOS", "REGULADORES DE VOLTAJE", "KIT DE ROBOTICA", "KIT DE ROBOTICA", "KIT DE ROBOTICA", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "INTERRUPTORES", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "CIRCUITOS INTEGRADOS", "TARJETAS ELECTRÓNICAS", "TARJETAS ELECTRÓNICAS", "SENSORES", "TARJETAS ELECTRÓNICAS", "SENSORES MEDIDOR D", "CARCASA DE PLASTICO", "SENSOR DE MICROFONO", "SENSORES", "SENSORES", "PARTE DE CAMARA", "SENSORES", "TARJETAS ELECTRÓNICAS", "TARJETAS ELECTRÓNICAS", "TARJETAS ELECTRÓNICAS", "TARJETAS ELECTRÓNICAS", "SENSORES", "MINI PANTALLA DISPLAY", "RELE", "TARJETAS ELECTRÓNICAS", "CABLES", "CABLES", "CABLES", "CABLES", "CABLES", "CABLES", "TARJETAS ELECTRÓNICAS", "SOPORTE PARA TARJETAS", "MINI PANTALLA DISPLAY", "MINI PANTALLA DISPLAY", "MINI PANTALLA DISPLAY", "REGULADORES DE VOLTAJE", "RECEPTOR INALAMBRICO", "TARJETAS ELECTRÓNICAS", "TARJETAS ELECTRÓNICAS", "KIT DE ROBOTICA", "MINI PANTALLA DISPLAY", "RECEPTOR INALAMBRICO"]
#saveProducto(mercan,id_w,sku,nombre,precio_compra,precio_neto,variacion,parent_id,categorias,imagen) #crear productos




# sku=['AA001', 'AA002', 'AA003', 'AC001', 'AC002', 'AC003', 'AC004', 'AC009', 'AG001', 'AG002', 'AO001', 'AG003', 'AG004', 'AG005', 'AG006', 'AG007', 'AG008', 'AG009', 'AG013', 'AG014', 'AG010', 'AG011', 'AG016', 'AG017', 'AG015', 'AO002', 'AO003', 'AO005', 'AO004', 'AO008', 'AO006', 'AO007', 'AS023', 'AS001', 'AS003', 'AS005', 'AS006', 'AS008', 'AS009', 'AS010', 'AS011', 'AS013', 'AS014', 'AS015', 'AS016', 'AS017', 'AS018', 'AS019', 'AS020', 'AS022', 'AS025', 'ME001', 'AS026', 'AS027', 'CO001', 'CO003', 'CO002', 'CO013', 'CO004', 'CO005', 'CO006', 'CO007', 'CO008', 'CO009', 'CO010', 'CO011', 'CO012', 'CO015', 'MA001', 'MA002', 'MD001', 'MD002', 'MD003', 'MD006', 'MD005', 'AU002', 'ME003', 'ME004', 'ME005', 'ME006', 'ME007', 'MI008', 'MI009', 'MI010', 'MI011', 'MI012', 'AC020', 'AC021', 'AC019', 'AC018', 'AC016', 'AC017', 'MI022', 'MI023', 'MI024', 'MI025', 'RR004', 'AC014', 'MO001', 'MO002', 'MO003', 'MO004', 'MO007', 'MO008', 'MO009', 'P1086', 'P1087', 'P1088', 'P1089', 'P1093', 'P1101', 'P1127', 'P1132', 'P1134', 'P1220', 'P1300', 'P1356', 'P1415', 'P1416', 'P1418', 'P1419', 'P1420', 'P1424', 'P1425', 'P1429', 'P1645', 'P2118', 'P2123', 'P2130', 'P2361', 'P2456', 'P2457', 'P2458', 'P2459', 'P2465', 'P2510', 'P2570', 'P2850', 'P2851', 'P3061', 'P3063', 'P3065', 'P3101', 'P3125', 'P3062', 'P713', 'P951', 'P960', 'P961', 'P975', 'P998', 'P999', 'PA001', 'PA002', 'PA003', 'PA004', 'PA005', 'PA006', 'PA007', 'PR001', 'PR002', 'PR003', 'RA001', 'RA002', 'RA003', 'RA004', 'RA005', 'RA006', 'RA007', 'RA009', 'RK003', 'RK005', 'RK006', 'RN001', 'RN002', 'RN003', 'RP002', 'RA017', 'RP003', 'RR001', 'RR002', 'RR003', 'SE001', 'SE002', 'SE003', 'SE004', 'SE005', 'SE006', 'SE007', 'SE008', 'SE009', 'SE010', 'SE011', 'SE012', 'SE013', 'SE014', 'SE015', 'SE016', 'SE017', 'SE018', 'SE019', 'SE021', 'SE022', 'SE023', 'SE024', 'SE026', 'SE027', 'SE028', 'SE029', 'SE030', 'SE033', 'SE038', 'SE032', 'P1696', 'SE036', 'AC015', 'MD004', 'SE037', 'CH001', 'PA008', 'RE001', 'P3126', 'P3073', 'P3074', 'P798', 'P3575', 'RP001', 'RP004', 'CO016', 'CO017', 'AS028', 'AS029', 'SE025', 'SE020', 'SE031', 'AC010', 'AC011', 'AC012', 'AC013', 'CO014', 'P1430', 'P3081', 'P2990', 'SE034', 'CO018', 'AS007', 'SE041', 'RE002', 'SE039', 'SE040', 'RR005', 'RP004-1', 'PA009-1', 'P2450', 'P3030', 'P1454', 'P1452', 'P3170', 'P3214', 'P3215', 'P3039', 'B11901', 'B09275', 'B10280', 'B09181', 'B08935', 'B09187', 'B18205', 'B11897', 'CH7637', 'B88962', 'B11900', 'B26452', 'B23821', 'B22906', 'SE042', 'CO019', 'FE001', 'FE002', 'NX001', 'NX002', 'PA010', 'NX004', 'NX003', 'P3071', 'P642', 'P3080', 'P2590', 'SE043', 'SE044', 'PR004', 'MI003', 'MI004', 'SE045', 'SE046', 'SE047', 'SE048', 'SE049', 'SE050', 'AG012', 'AC005', 'MO010', 'SE051', 'SE052', 'SE053', 'AC022', 'CO020', 'PR005', 'MO011', 'MO012', 'MO013', 'MO014', 'MO015', 'MO016', 'MO017', 'MO018', 'MO019', 'MO020', 'MA003', 'RA008', 'RA010', 'CH005', 'CH21044', 'B110537', 'B26738', 'B41271', 'B20386', 'B9964', 'B64210', 'B9273', 'B88955', 'MD007', 'MD008', 'AU001', 'MI001', 'MD009', 'AS030', 'AS031', 'RP001-1', 'P799', 'P1572', 'P1573', 'P3203', 'P3202', 'P3075', 'P950', 'P953', 'FT001', 'FT002', 'FT003', 'FT004', 'FT005', 'FT021', 'FT023', 'FT022', 'FT030', 'FT031', 'FT052', 'FT051', 'FT071', 'FT072', 'FT006', 'AG019', 'AG020', 'SE054', 'SE055', 'SE056', 'MI002', 'MO005', 'CO021', 'SE057', 'ME008', 'ME009', 'ME010', 'MD010', 'MI005', 'MI006', 'MI007', 'MO021', 'MD011', 'SE058', 'AS032', 'AS033', 'CO022', 'CID001', 'CID002', 'SE059', 'MI027', 'MI026', 'RE003', 'RE004', 'EP001', 'EP003', 'EP003-10', 'EP003-22', 'EP003-47', 'EP003-100', 'EP003-150', 'EP003-200', 'EP003-220', 'EP003-270', 'EP003-330', 'EP003-470', 'EP003-510', 'EP003-680', 'EP003-1k', 'EP003-2.2k', 'EP003-3.3k', 'EP003-4.7k', 'EP003-5.1k', 'EP003-6.8k', 'EP003-10k', 'EP003-20k', 'EP003-47k', 'EP003-51k', 'EP003-68k', 'EP003-100k', 'EP003-220k', 'EP003-300k', 'EP003-470k', 'EP003-680k', 'EP003-1m', 'CO023', 'CT001', 'CT002', 'MO022', 'SE060', 'CH004', 'SE061', 'SE062', 'AU003', 'MD012', 'CH002', 'RK004', 'BT001', 'SE063', 'ME002', 'RK007', 'MA004', 'MA005', 'EP004', 'EP004-1k', 'EP004-1m', 'EP004-10k', 'EP004-10', 'EP004-100k', 'EP004-100', 'EP004-1.5k', 'EP004-2.2k', 'EP004-15k', 'EP004-22', 'EP004-10m', 'EP004-220', 'EP004-3.3k', 'EP004-330k', 'EP004-330', 'EP004-5.6k', 'EP004-47k', 'EP004-47', 'EP004-470k', 'EP004-470', 'EP004-4.7k', 'EP004-56k', 'EP004-560', 'EP004-6.8k', 'EP004-68k', 'EP004-680k', 'EP004-680', 'EP004-1', 'EP004-22k', 'EP004-33k', 'EP005', 'EP005-1', 'EP005-10', 'EP005-22', 'EP005-47', 'EP005-100', 'EP005-220', 'EP005-330', 'EP005-470', 'EP005-560', 'EP005-680', 'EP005-1k', 'EP005-1.5k', 'EP005-2.2k', 'EP005-3.3k', 'EP005-4.7k', 'EP005-5.6k', 'EP005-6.8k', 'EP005-10k', 'EP005-15k', 'EP005-22k', 'EP005-33k', 'EP005-47k', 'EP005-56k', 'EP005-68k', 'EP005-100k', 'EP005-330k', 'EP005-470k', 'EP005-680k', 'EP005-1m', 'EP005-10m', 'EP006', 'EP007', 'EP006-1', 'EP006-2', 'EP006-3', 'EP006-4', 'EP006-5', 'EP006-6', 'EP006-7', 'EP006-9', 'EP006-8', 'EP007-1', 'EP007-2', 'EP007-3', 'EP007-4', 'EP007-5', 'EP007-6', 'EP007-7', 'FE003', 'EA001', 'EA001-1', 'EA002', 'EA002-1', 'EA002-2', 'EA002-3', 'EA003', 'EA003-5', 'EA003-4', 'EA004', 'EA004-1', 'EA004-2', 'EA005', 'EA005-1', 'EA005-2', 'EA005-3', 'EA005-4', 'EA005-5', 'EA006', 'EA006-1', 'EA006-2', 'EA006-3', 'EA006-4', 'EA007', 'EA007-2', 'EA007-3', 'EA007-4', 'EA007-5', 'EA007-6', 'EA007-1', 'EA008', 'EA009', 'EP008', 'EP008-100k', 'EP008-50k', 'EP008-10k', 'EP008-5k', 'EP008-1k', 'EP009', 'EP009-100k', 'EP009-10k', 'EP009-1k', 'EP009-100', 'MO023', 'MI028', 'EA010', 'EA010-1', 'EA010-2', 'EP010', 'EP010-1', 'EP010-2', 'uC001', 'EP011', 'EP011-1', 'EP011-2', 'EP012', 'EP012-1', 'EP012-2', 'EP013', 'EP013-1', 'EP013-2', 'EP014', 'EP014-1', 'EP014-2', 'EP015', 'EP016', 'ME011', 'RE005', 'SE064', 'AC023', 'AC024', 'AC025', 'CI7400', 'CI7402', 'FE010', 'FE011', 'SE065', 'SE066', 'SE067', 'PA011', 'PA011-1', 'PA011-2', 'MI013', 'CO024', 'RE006', 'SE068', 'AK001', 'CO025', 'CO026', 'CI7404', 'CI7408', 'CI7411', 'CI7421', 'CI7427', 'CI7432', 'CI7447', 'CI7448', 'CI7473', 'CI7474', 'CI7485', 'CI7483', 'CI7486', 'CI7493', 'CI74107', 'CI74139', 'CI74153', 'CI74157', 'CI74192', 'CI4013', 'CI4015', 'CI4027', 'CI4029', 'CI4042', 'CI4052', 'CI40106', 'CI003', 'CI004', 'CI005', 'CI006', 'CI007', 'CI008', 'CI009', 'CI010', 'CI011', 'SE069', 'SE037-1', 'CH006', 'AG021', 'AG022', 'P989', 'P1695', 'P791', 'P2507', 'P2096', 'B9490', 'B178009', 'P2117', 'P4101', 'P4201', 'P4401', 'P4301', 'P4501', 'P4601', 'CO027', 'SE070', 'SE071', 'CO028', 'AU004', 'AU005', 'SE072', 'SE073', 'SE074', 'CO029', 'AG023', 'AG024', 'FE004', 'FE005', 'AK004', 'AK005', 'RK008', 'AK003', 'AK006', 'P3072', 'P3239', 'FT008', 'FT007', 'AC026', 'CI012', 'SE075', 'uC002', 'MI030', 'SE076', 'MD013', 'AS024', 'AS004', 'NX005', 'ST001', 'ST002', 'ST003', 'ST004', 'B26739', 'P1000', 'P3060', 'P3172', 'P3064', 'MO025', 'CO030', 'FE006', 'MI031', 'EP017', 'EP018', 'MO024', 'AU006', 'MI029', 'RA012', 'AVE001', 'AS034', 'RA013', 'RA014', 'NX006', 'RK009', 'MO026', 'MI014', 'MI015', 'MI016', 'ST005', 'ST006', 'ST007', 'RP005', 'RA015', 'RA016', 'RA018', 'NV001', 'CO031', 'MI032', 'MI032-1', 'MI032-2', 'MI032-3', 'MI033', 'MI033-1', 'MI033-2', 'MI033-3', 'MI034', 'P2999', 'P2997', 'P2520', 'RP006', 'RP007', 'P4843', 'P3037', 'EA003-3', 'EA003-1', 'EA003-2', 'EA004-4', 'EA004-3', 'EA013', 'EA013-2', 'EA013-1', 'EA014', 'EA014-2', 'EA014-1', 'EA012', 'EA012-3', 'EA012-2', 'EA012-1', 'uC006', 'uC004', 'uC005', 'uC009', 'uC007', 'uC008', 'uC003', 'EP004-2.7k', 'EP004-150k', 'EP004-510k', 'EP004-2.2m', 'EP004-4.7m', 'EP006-10', 'EP020', 'EP020-1', 'EP020-2', 'EP020-3', 'EP020-4', 'EP019', 'EP019-1', 'EP019-2', 'EP002', 'EP002-1', 'EP002-2', 'EP002-3', 'EP002-4', 'EP002-5', 'EP008-20k', 'EP021', 'EP021-6', 'EP021-7', 'EP021-8', 'EP021-9', 'EP021-10', 'EP021-5', 'EP021-4', 'EP021-3', 'EP021-2', 'EP021-1', 'EP010-4', 'EP010-3', 'CI002', 'MI035', 'MI035-2', 'MI035-3', 'MI035-4', 'MI036', 'MI036-2', 'MI036-3', 'MI036-4', 'MI036-1', 'MI040', 'EP022', 'EP022-1', 'EP022-2', 'EP023', 'EP024', 'EP014-3', 'EP014-4', 'EP030', 'AC027', 'MI041', 'HE012', 'HE013', 'MI044', 'MI045', 'MI046', 'MI046-2', 'MI046-1', 'HE010', 'MI037', 'EP031', 'EP031-1', 'EP031-2', 'MI049', 'MI050', 'HE003', 'CH010', 'CH011', 'HE001', 'HE002', 'HE005', 'HE006', 'HE008', 'PI001', 'PI002', 'PI003', 'PI004', 'PI005', 'MI039', 'SE077', 'MI062', 'MI038', 'MI048', 'MI048-1', 'MI051', 'MI051-1', 'MI051-2', 'CI013', 'CI014', 'CI015', 'CI016', 'EA011', 'EA011-1', 'EA011-2', 'MI053', 'MI053-6', 'MI053-7', 'MI053-5', 'MI053-4', 'MI053-3', 'MI053-2', 'MI053-1', 'MI055', 'MI055-2', 'MI055-1', 'MI056', 'MI057', 'EP025', 'EP025-3', 'EP025-2', 'EP025-1', 'EP026', 'MI058', 'MI059', 'MI060', 'MI061', 'MI061-4', 'MI061-3', 'MI061-2', 'MI063', 'EP032', 'EP032-1', 'EP032-2', 'EP033', 'EP034', 'HE014', 'MI064', 'MI046-3', 'EA015', 'EP005-560k', 'EP005-820', 'EP005-8.2k', 'EP005-82k', 'EP005-820k', 'MI053-8', 'RA019', 'RA020', 'ST008', 'MI065', 'HE015', 'HE016', 'HE017', 'HE018', 'SE078', 'SE079', 'PA012', 'MD014', 'SE080', 'HE020', 'RE007', 'FE012', 'SE082', 'RK002', 'SE081', 'HE021', 'HE022', 'CO032', 'MI066', 'RE008', 'SE083', 'SE084', 'AC028', 'EP019-3', 'EP035', 'EP035-4', 'EP035-5', 'EP035-3', 'EP035-2', 'EP035-1', 'MI063-1', 'MI063-2', 'MI062-1', 'MI062-2', 'MI046-5', 'MI046-4', 'HE023', 'HE024', 'HE025', 'HE025-1', 'HE025-2', 'HE026', 'EP008-500k', 'EA003-6', 'EA016-1', 'EA016-2', 'AA004', 'SE085', 'SE056-2', 'MI017', 'MI036-5', 'MI036-6', 'MI036-7',]

# for i in range(len(sku)):
#     r=wcapi1.get("products",params={'sku':sku[i]}).json()
#     print("Producto simple del producto")
#     print("",r[0].get('name'))
#     print("",r[0].get('price'))
#     print("",r[0].get('parent_id'))
#     r1=wcapi1.get("products/"+str(r[0].get('id'))+"/variations").json()
#     print("Variaciones del producto",len(r1))
   
    
#     print()
#     print("###############################################################################################")
#     print()
#print(len(r),r[0].get('id'),r[0].get('name'))
# id=[29,30,31,32,33,34]
# v=[]
# for i in range(len(id)):
#     p =wcapi.get("products/"+str(id[i]))
#     p1=p.json()
#     v.append(p1)
#     print(p1.get('name'), p1.get('sku') ,id[i])
# with open('dataPrueba.json', 'w') as fp:
#     json.dump(v, fp)
# with open('dataPrueba.json', 'r') as fp:
#     data = json.load(fp)
# print(data[0].get('name'))
# print(type(data))
    

    #print(wcapi1.put("products/"+str(id),data)


#Permite realizar
def buscarProductos(request,id,idas,idfa):
    print("estoy denr¡ntro de crear importAIOCN")
    if request.method == 'POST':
        print("estoy denr¡ntro de crear importAIOCN")

        list_sku = request.POST.get('skus')
        print(list_sku)
        productos=buscarSKU(list_sku)
        print(productos)
        print(productos)
        datos={
                "id":id,
                "idas":idas,
                "idfa":idfa

        }
        productos.update(datos)
    return render(request, 'core/crear_importacion.html', productos )


def startImport(request):
    imp=Importacion(fecha=str(datetime.datetime.today()).split()[0],descripcion="",tipo="",origen="",estado=0)
    imp.save()
    print("estoy creando la importacion")
    id_impor=Importacion.objects.last()
    id=id_impor.id
    print("estoy creando la importacion1")
    print("valor de l id ", id)
    
    return redirect('importacion',id)


# Create your views here.
def conexionApiWoo():
    
    wcapi = API(
        url="http://18.217.125.242/", # Your store URL
        consumer_key="ck_683236fc573061c7e21af53d9c73a53a8f205229", # Your consumer key
        consumer_secret="cs_767e7406490a81353255b4937c055ca1036c5dbf", # Your consumer secret
        wp_api=True, # Enable the WP REST API integration
        version="wc/v3" # WooCommerce WP REST API version
    )
    products = wcapi.get("products")
    productos=products.json()

    print(products.status_code)
    #print(productos[2])
    print('----------------------')
    
#     id=productos[0].get('id')
#     sku=productos[0].get('sku')
#     name=productos[0].get('name')
#     type=productos[0].get('type')
#     description=productos[0].get('description')
#     price=productos[0].get('price')
#     regular_price=productos[0].get('regular_price')
#     sale_price=productos[0].get('sale_price')
#     categories=productos[0].get('categories')#.name
#     image=productos[0].get('images')#.src
#     print("puchase_price: ",productos[0].get('purchase_price'))
#     print("id : ",id)
#     print("sku : ",sku)
#     print("name : ",name)
#     print("type : ",type)
#     print("description : ",description)
#     print("price : ",price)
#     print("regular peice : ",regular_price)
#     print("sale price : ",sale_price)
#     print("categories : ",categories)
#     print("images : ",image)


#     print(productos[0].get('id'))

# #1602

#     id=productos[0].get('id')
#     data = {
#         "regular_price": "88888"
#     }


#     #wcapi.put("products/"+str(id),data)
#     print(productos[0].get('id'))

    return productos

def inicio(request):
    return render(request,'core/inicio.html')
def home(request):
   

    return render(request,'core/home.html')

def login(request):
    return render(request,'core/login.html')
 

def detalleImportacion(request,id,idas,idfa):
    datos={ "id":id,
            "idfa":idfa,
            "idas":idas }
    

    return render(request,'core/detalle_importacion.html',datos)
 



def password(request):
    return render(request,'core/password.html')

def calcular(request):
    if "id_producto" in request.POST:
        product_id=request.POST.getlist('id_producto')
        print(product_id)
        precio=request.POST.getlist('precio')
        proveedor=request.POST.getlist('proveedor')
        cantidad=request.POST.getlist('cantidad')
        
        mercancia=request.POST.getlist('mercancia')
        peso=request.POST.getlist('peso')

        saveDetalleImportacion(peso,precio,cantidad,product_id,mercancia,proveedor)

       
    return HttpResponse("<h1>"+str(product_id)+"</h>")

def register(request):
    if request.method=='POST':
        print('segundo formulaei')
        form=UserRegisterForm(request.POST)
        print(form)
        pas=form['password1'].value()
        username=form['password2'].help_text
        print("ddddddddddddddddddddddddd",username)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha registrado correctamente!')
            return redirect(request,'core/register.html')
        else: 
            form=UserRegisterForm()
            messages.success(request, 'No se ha podido registrar! La clave de contener numeros, letras mayusculas y minusculas, y debe contener mas de 8 carateres ')
            context={
                'form':form
            }
        return render(request,'core/register.html',context)
    else:
        
        form=UserRegisterForm()
    
        context={
                'form':form
            }
    print(context)
    return render(request,'core/register.html',context)

def saveProduct(request):
    if request.method=='POST':
        form=ProductRegister(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha registrado correctamente!')
            return render(request,'core/product.html')
        else: 
            form=ProductRegister()
            messages.success(request, 'No se ha podido registrar! ')
            context={
                'form':form
            }
        return render(request,'core/product.html',context)
    else: 
        form=ProductRegister()
    
        context={
                'form':form
            }
    print(context)
    return render(request,'core/product.html',context)



def importacion(request,id):
    print("estoy dentro del editar")
    datos = Importacion.objects.get(id=id)  
    context={
                'form':FormImportacion(instance=datos)
            }
    if request.method=='POST':
        form=FormImportacion(request.POST,instance=datos)
        if form.is_valid():
            fecha=form['fecha'].value()
            form.save()
            
            cantidad=request.POST.get('cantidad')
            cant=[]
            proveedor=Proveedor.objects.last()
            importacion=Importacion.objects.get(id=id)
            fac=Factura_proveedor.objects.filter(importacion=id)
            if(len(fac) < int(cantidad)):
                print(len(fac),int(cantidad))
                print(len(fac)-int(cantidad))
            
                for k in  range(int(cantidad)-len(fac)):
                    pf=Factura_proveedor(proveedor=proveedor,importacion=importacion,num_cajas=0,valor_factura=0,valor_envio=0,comision_envio=0,isd=23333,total_pago=0,extra=0)
                   
                    
                    pf.save()
            
                
            
            messages.success(request, 'Se ha registrado correctamente!')
            return redirect('startFP',id)
            
            #return render(request,'core/proveedor.html',{"cantidad":cant,"cant":cantidad,"proveedores":proveedores,'fecha':fecha})

    return render(request,'core/importacion.html',context)
# def actualizar(request,id):
#     datos = Importacion.objects.get(id=id) 
#     form=FormImportacion(request.POST,instance=datos) 
#     if form.is_valid():
#         form.save()
#         fecha=form['fecha'].value()
#         proveedores=Proveedor.objects.select_related().all()
#         cantidad=request.POST.get('cantidad')
#         cant=[]
#         for k in  range(int(cantidad)):
#             cant.append(k)
#         print(cantidad)
        
#         messages.success(request, 'Se ha registrado correctamente!')
#     return render(request,'core/proveedor.html',{"cantidad":cant,"cant":cantidad,"proveedores":proveedores,'fecha':datos})
    






