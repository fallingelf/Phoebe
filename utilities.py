# -*- coding: utf-8 -*-


def files(keys,path=None,isfile=1,isre=0,ismerg=1,iswt=0):
    '''
    Created on Thu Nov 22 22:14 2018
    files(keys,path='NotPath',isfile=1,isre=0,ismerg=1,iswt=0)
    
        从特定目录下找到含有keys的文件
    
    parameter:
    ---------
    keys    以逗号(,)标记为分离的字符串变量
            在非正则模式下，* 表示通配符
    
    Optional keyword arguments:
    path    搜索的目录，默认为当前目录
    isfile  目标文件类型
            0--文件夹
            1--文件 (default)
            2--所有
            默认--文件
    isre    keys是否是正则表达式
            0--不是 (default)
            1--是
            默认--不是
    ismerg  是否合并满足条件的文件为单一列表
            0--不合并
            1--合并 (default)
            默认--合并
    iswt    是否将列表写入文件，文件名为keys中的单词字符组合
            0--不写入 (default)
            1--写入
            默认--不写入
            
    return:
    ------
    filter_files: list
        符合条件的文件列表
        
    Example:
    -------
        files('*.py,d*')   #找到当前目录先所有以'.py'结尾的文件和以'd'开头的文件
    
    @author: wqs
    '''

    import os,re
    
    filter_files=[]
    if path==None: 
        path=os.getcwd();
    pwd=os.getcwd(); os.chdir(path);
        
    all_files=os.listdir(path)
    if isfile==0:
        obj_files=[all_files[i] for i in range(len(all_files)) if os.path.isdir(all_files[i])]
    elif isfile==1:
        obj_files=[all_files[i] for i in range(len(all_files)) if os.path.isfile(all_files[i])]
    else:
        obj_files=all_files
    #obj_files=' '.join(list(obj_files))
    for key in keys.replace(',',',^').split(','):
        if not isre:
            key=key.replace('.','\.').replace('*','[\S]*')
        key=key+'$';
        filter_files.append([obj_files[i] for i in range(len(obj_files)) if re.findall(re.compile(key),obj_files[i])])
    if ismerg:
        filter_files_all=[]
        for filter_files_i in filter_files:
            filter_files_all=filter_files_all+filter_files_i
        filter_files=sorted(list(set(filter_files_all)))
        while '' in filter_files:
            filter_files.remove('')
    if iswt:
        with open(keys.replace('*','').replace('.','').replace(',','_').replace(' ','')+'.txt','w+') as hd:
            if ismerg:
                hd.write(str('\n'.join(filter_files)+'\n'));
            else:
                hd.write(str(filter_files));
            hd.close()
    
    os.chdir(pwd)
    return sorted(filter_files)


def rm(file):
    '''
    Created on 2019/1/10
    
    rm(file)
        删除当前文件夹下的文件(夹)
    
    paremeter:
    ---------
    file: str
        文件(夹)名
    
    return:
    ------
    有此没有此文件，直接返回-1
      有此文件夹，删除并返回0
        有此文件，删除并返回1
        
    Example:
    -------
        rm('ss.txt')  #删除文件
        rm('ss')      #删除文件夹
    
    @author: wqs
    '''

    import os,shutil
    if os.path.exists(file):
        if not os.path.isdir(file):
            os.remove(file)
            return 0
        else:
            shutil.rmtree(file)
            return 1
    return -1


def mkdir(folder):
    '''
    Created on Tue May 21 09:56:58 2019
    mkdir(folder)：
        新建一个文件夹，如果存在则不执行操作
    
    parameters:
    ----------
    folder: str
        文件夹名称
    
    return:
    ------
    isnew: int
        如果文件夹存在，则返回0
                不存在,则返回1

    @author: wqs
    '''
    import os
    isnew=0
    if not os.path.exists(folder):
        os.mkdir(folder)
        return 1
        
    return isnew
        

def implot(fits_img,col=None,row=None,figsize=(30,20),dataHDU=0,cmap=None,fig=[],ax=[],fmt='k-'):
    """
    Created on Mon Dec 16 19:58:27 2019
     
        plot the data of fits or 1D (2D) array
    
    parameter:
    ---------
    fits_img: str or darray
        the name of fits file or 1D (2D) array
    
    col: None,int,'+'
        specified which col to draw
        
    row: None,int,'+'
        specified which row to draw
        
    figsize: tuple
        specified the size of the layer
        
    dataHDU: int
        which HDU of the fits file contains the data 
        
    return:
    ------
    fig,ax
    
    @author: wqs
    """
    
    from astropy.io import fits
    import matplotlib.pyplot as plt
    
    if fig==[]: fig=plt.figure(figsize=figsize) 
    if ax==[]: ax=plt.gca()
    
    if isinstance(fits_img,str):
        with fits.open(fits_img) as hdu:
            hdd=hdu[dataHDU].data
    else:
        hdd=fits_img
        
    if len(hdd.shape)==1:
        ax.plot(hdd,fmt)
    else:
        if isinstance(col,int):
            ax.plot(hdd[:,col], fmt, label='column#'+str(col))
        elif col == '+':
            ax.plot(hdd.sum(axis=0), fmt, label='the sum of the column')
        elif col!=None:
            print('can not identify the value of col')
            
        if isinstance(row,int):
            ax.plot(hdd[row,:], fmt, label='row#'+str(row))
        elif row == '+':
            ax.plot(hdd.sum(axis=1), fmt, label='the sum of the row')
        elif row!=None:
            print('can not identify the value of row')
        
        if (col==None) and (row==None):
            import matplotlib.cm as cm
            if cmap==None: cmap=cm.hot
            plt.imshow(hdd, origin='lower',aspect='auto',cmap=cmap)
    
    if (col!=None) and (row!=None): plt.legend()

    return fig,ax      
        
def savenarry(array_list,file_out='dnarray.csv'):
    '''
    save a list of array to file <file_out>
    
    sample:
        savenarry([x,y],file_out='dnarray.csv')
    '''
    
    from pandas import DataFrame
    from numpy import vstack
    
    array_list=vstack(array_list)
    fp=DataFrame(array_list.T)
    fp.to_csv(file_out,index=False,header=False,sep=",")
    
    return None

def smooth(x,window_len=11,window='hanning'):
    '''
    smooth a 1d array with the window of the specified length 
    
    sample:
        smooth(x,window_len=11)
    '''
    
    import numpy as np
    
    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len<3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y[(window_len//2):-(window_len//2)]

def PMD(x,y,dy,pVal,mode="period",label=None,figout=None,pmd_para=[10,3]):  
    '''
    >x,y,dy 时间，星等，误差
    >pVal:[最小周期，最大周期，周期间隔]
    >label-----figout--------outdir 
     曲线解释---图片保存名称---图片保存目录
    >作图：原始数据，周期theta图，相位图
    '''
    
    import numpy as np
    import matplotlib.pyplot as plt 
    from PyAstronomy.pyTiming import pyPDM 

    if not isinstance(x,np.ndarray): 
        x=np.array(x);y=np.array(y);dy=np.array(dy);
    S = pyPDM.Scanner(minVal=pVal[0], maxVal=pVal[1], dVal=pVal[2], mode=mode)
    P = pyPDM.PyPDM(x, y)
    time, theta = P.pdmEquiBinCover(pmd_para[0], pmd_para[1], S);
    
    fig, ax = plt.subplots(3)
    fig.set_size_inches(30,20)
    ax[0].invert_yaxis();ax[2].invert_yaxis();
    ax[0].grid();ax[1].grid();ax[2].grid();
    ax[0].errorbar(x,y,dy,fmt='o');    
    ax[0].legend([label],loc='upper right',fontsize=20,frameon=False)

    ax[1].set_title("Result of PDM analysis");ax[1].set_xlabel(mode);ax[1].set_ylabel("Theta")
    ax[1].plot(time, theta, 'bp-');
    
    best_period = time[np.argmin(theta)];
    peak_theta=np.min(theta)
    ax[1].plot(best_period,peak_theta,'ro')
    ax[1].legend(['pdmEquiBinCover','peak is '+str(round(best_period,10))+'d'],loc='lower right',fontsize=15,frameon=False)
    
    if mode=="period":
        ax[2].errorbar((x/best_period)%1,y,dy,fmt='o')
    else:
        ax[2].errorbar((x*best_period)%1,y,dy,fmt='o')
    ax[2].legend(['folded data with period='+str(round(best_period,10))+'d'],loc='upper right',fontsize=20)
    if figout != None:
        plt.savefig(figout,dpi=600)
    plt.show()
    return time, theta, best_period

def LSP(x,y,dy,fVal=[0,1,5,1],norm='standard',figout=None,label=None,freq_set=None):  
    '''
    周期分析
    https://docs.astropy.org/en/stable/timeseries/lombscargle.html#periodogram-algorithms

    参数：
    x,y,dy: arrays
        时间，星等，误差
    figout: str
        图片保存名称
    fVal: list
        minimum_frequency,maximum_frequency,samples_per_peak(default 5),nterms(default 1)
    
    return:
        frequency, power, residuals, x_range, y_fit, theta
        if nterms=1:
            theta=[off_set,amplitude,phi,best_frequency]
            y=off_set+amplitude*np.sin(2*np.pi*best_frequency*x+phi)
    '''
    import numpy as np
    import matplotlib.pyplot as plt 
    from astropy.timeseries import LombScargle
    
    if not isinstance(x,np.ndarray): 
        x=np.array(x);y=np.array(y);dy=np.array(dy);
    fVal[0]=10**-5 if fVal[0]==0 else fVal[0]
    ls=LombScargle(x, y, dy, nterms=fVal[-1], normalization=norm)
    frequency, power =ls.autopower(minimum_frequency=fVal[0],maximum_frequency=fVal[1],samples_per_peak=fVal[2])
    
    fig, ax = plt.subplots(3)
    fig.set_size_inches(20,27)
    #ax[0].invert_yaxis();ax[2].invert_yaxis();
    ax[0].grid();ax[1].grid();ax[2].grid();
    ax[0].errorbar(x,y,dy,fmt='bo-',label=label);    
    ax[1].set_xlim((frequency[0],frequency[-1]))
    ax[1].plot(frequency,power,'b-')
    ax11=ax[1].twiny()
    ax11.set_xlim(ax[1].get_xlim())
    x_side=np.linspace(0.001+frequency[0],frequency[-1],10)
    x_side_var=np.round(24*60/x_side,2)
    plt.xticks(x_side,x_side_var,rotation=0) 

    best_frequency = frequency[np.argmax(power)]
    peak_power=power.max()
    ax[1].plot(best_frequency,peak_power,'ro')
    ax[1].legend(['spectrum distribution','peak frequency '+str(round(best_frequency,4))+'c/d is period '+str(round(24/best_frequency,4))+'h'],loc='upper right',fontsize=15,frameon=False)
    if fVal[-1]==1:
        for cutoff in ls.false_alarm_level([0.1, 0.05, 0.01]) :
            ax[1].axhline(cutoff, color='black', linestyle='dotted')
    if freq_set!=None: best_frequency=freq_set
    phase=(x*best_frequency)%1
    y_fit=ls.model(x,best_frequency)
    residuals=y-y_fit
    y_fit=y_fit[np.argsort(phase)]
    ax[2].plot(np.sort(phase),y_fit,'r-',linewidth=5)
    ax[2].errorbar(phase,y,dy,fmt='b.',alpha=1)
    ax[2].legend(['best fitted curve is '+str(best_frequency),'folded data'],loc='upper right',fontsize=15,frameon=False)
    
    x_range=np.linspace(x.min(),x.max(),100)
    y_fit=ls.model(x_range,best_frequency)
    ax[0].plot(x_range,y_fit,'r-',label='fitting curve',linewidth=5)
    ax[0].legend(loc='upper right',fontsize=15,frameon=False)

    if figout: plt.savefig(figout,dpi=100)
    plt.show()
    
    if fVal[-1]==1:
        print('the false alarm probability for %0.2f (%0.2f min) is %0.2e'%(best_frequency,24*60/best_frequency,ls.false_alarm_probability(peak_power,method='davies')))
    
    theta = ls.model_parameters(best_frequency)
    theta[0]=ls.offset()+theta[0]
    if len(theta)==3:
        K=(theta[1]**2+theta[2]**2)**0.5
        phi=np.arcsin(theta[2]/K)
        theta=[theta[0],K,phi,best_frequency]

    return frequency,power,residuals,x_range,y_fit,theta
    
def WD_MR(M1):
    '''
    the relation of mass and radius for a white dwarf
    with respect to the parameters of the solar
    Nauenberg 1972
    '''
    if not isinstance(M1,(int,float)):
        M1=(M1.to('solMass')).value
        
    R1=7.79*10**8*((1.44/M1)**(2/3)-(M1/1.44)**(2/3))**0.5*u.cm
    
    return (R1.to('solRad')).value

def RD_MR(M2):
    '''
    the relation of mass and radius of the donor in cataclysmic variables 
    with respect to the parameters of the solar
    doi:10.1093/mnras/stz976 
    '''
    if not isinstance(M2,(int,float)):
        M2=(M2.to('solMass')).value
        
    Mbounce=0.063
    Mconv=0.2
    Mevol=0.8
    if M2<Mbounce:
        R2=0.109*(M2/Mbounce)**0.152
    elif (M2<=Mconv) & (M2>=Mbounce):
        R2=0.225*(M2/Mconv)**0.636
    elif (M2>Mconv) & (M2<=Mevol):
        R2=0.293*(M2/Mconv)**0.69
    else:
        sys.exit('M2 is out the range (M2 <= 0.8 M_sun)')
    return R2

def RD_RM(R2):
    '''
    the relation of mass and radius of the donor in cataclysmic variables 
    with respect to the parameters of the solar
    doi:10.1093/mnras/stz976 
    '''
    if not isinstance(R2,(int,float)):
        R2=(R2.to('solRad')).value
        
    Mbounce=0.063
    Mconv=0.2
    Mevol=0.8

    M2_boun=(R2/0.109)**(1/0.152)*Mbounce
    M2_conv=(R2/0.225)**(1/0.636)*Mconv
    M2_evol=(R2/0.293)**(1/0.69)*Mconv
    if M2_boun<Mbounce:
        M2 = M2_boun
    elif (M2_conv<=Mconv) & (M2_conv>=Mbounce):
        M2 = M2_conv
    elif (M2_evol>Mconv) & (M2_evol<=Mevol):
        M2 = M2_evol
    else: 
        sys.exit('M2 is out the range (M2 <= 0.8 M_sun)')
    return M2
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        
        
        