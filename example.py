import matplotlib.colors
import netCDF4
import numpy as np
from datetime import datetime
# import cartopy.crs as ccrs
import pyresample
import matplotlib.pyplot as plt
from pycoast import ContourWriterAGG
import aggdraw
############################read the nc file###########################################
# do loop
hour = ['14']#,'03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
min = ['00']#,'10','20','30','40','50']
# shapePath = 'F:/H8/gshhg-shp-2.3.7/'
# ttfFile = 'F:/H8/LiberationMono-Regular.ttf'

for i in hour:
    for j in min:

        # Modify name and get the correct file
        dtime = datetime(2018, 5, 28, int(i), int(j))                                  #修改時間
        dir = './data/'
        ncfile = dir + 'NC_H08_20180528_' + i + j + '_R21_FLDK.06001_06001.nc'          #修改時間
        data = netCDF4.Dataset(ncfile)
        #print(data)
        #exit()

        # Extract datas
        lat = data['latitude'][:]
        lon = data['longitude'][:]
        lons, lats = np.meshgrid(lon, lat)
        b03 = data['albedo_03'][:]
        b05 = data['albedo_05'][:]
        b04 = data['albedo_04'][:]
        b06 = data['albedo_06'][:]
        b11 = data['tbb_11'][:]
        b13 = data['tbb_13'][:]
        b14 = data['tbb_14'][:]
        SOZ = data['SOZ'][:]

        # TODO 
        # Interesting data location
        lats = lats[1550:2050, 1800:2300]
        lons = lons[1550:2050, 1800:2300]
        b03 = b03[1550:2050, 1800:2300]
        b04 = b04[1550:2050, 1800:2300]
        b05 = b05[1550:2050, 1800:2300]
        b06 = b06[1550:2050, 1800:2300]
        SOZ = SOZ[1550:2050, 1800:2300]
        b11 = b11[1550:2050, 1800:2300]
        b13 = b13[1550:2050, 1800:2300]
        b14 = b14[1550:2050, 1800:2300]

#print(lons.max(),lons.min())
#####################################################################

        dsize = 1800
        arraysize = dsize*dsize
        cnts = np.fromfile(ncfile, dtype='uint8')[-arraysize:].reshape(dsize,dsize)

#####################################################################
        from PIL import Image, ImageOps

# lots of hot spot RGB recipe

        # hot spot(fire)
        # CIRA's Nature fire color RGB
        #RGB = np.zeros((b03.shape[0],b03.shape[1],3),dtype='uint8')
        #RGB[:,:,0] = 255.0*((b06-0.0)/(1.0-0.0)).clip(0.0,1.0)
        #RGB[:,:,1] = 255.0*((b04-0.0)/(1.0-0.0)).clip(0.0,1.0)
        #RGB[:,:,2] = 255.0*((b03-0.0)/(1.0-0.0)).clip(0.0,1.0)

        # simple fire & smoke RGB
        #RGB = np.zeros((b03.shape[0],b03.shape[1],3),dtype='uint8')
        #RGB[:,:,0] = 255.0*((b07-287.02)/(425.26-287.02)).clip(0.0,1.0)
        #RGB[:,:,1] = 255.0*((b03-0.05)/(0.7-0.05)).clip(0.0,1.0)
        #RGB[:,:,2] = 255.0*((b13-230.3)/(302.71-230.3)).clip(0.0,1.0)

        # Aki Version
        #RGB = np.zeros((b05.shape[0],b05.shape[1],3),dtype='uint8')
        #RGB[:,:,0] = 255.0*((b07-286.78)/(345.38-286.78)).clip(0.0,1.0)
        #RGB[:,:,1] = 255.0*((b06-0.0)/(1.0-0.0)).clip(0.0,1.0)
        #RGB[:,:,2] = 255.0*((b05-0.0)/(1.0-0.0)).clip(0.0,1.0)

        # Jochen Version

        #L[:,:] = 255.0*((b15-273.0)/(350.0-273.0)).clip(0.0,1.0)

        b04 = b04 / np.cos(SOZ)
        b03 = b03 / np.cos(SOZ)
        NDVI = (b04 - b03) / (b04 + b03)
        PV = ((NDVI - NDVI.min()) / (NDVI.max() - NDVI.min())) ** 2
        emis = 0.004 * PV + 0.986
        K2 = 0.0143876869 / (11.2395 / 1000000)
        K1 = (1.19104356 / (10 ** 16)) / (((11.2395 / 1000000) ** 5) * 1000000)

        Rad = K1 / (np.exp(K2/b14) - 1)

        T = K2 / np.log((K1*emis/Rad) + 1)



###################################################################################


        # img.save('C:/CWBpython/setdata/CWBproject/image/20191230_' + i + j +       #修改時間
        #         '_06001_fireRGB_Jochen_smalldomain.jpg',
        #         format='JPEG', subsampling=0, quality=100)

        plt.imshow(T)
        plt.title("Himawari-8_LST_retrieval_Taiwan")
        plt.colorbar()
        plt.show()
        #img.show()

