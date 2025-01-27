def lang(choose):
    """多语言支持"""

    if choose == 0:
        # 英文词条
        version = 'version 0.1.2'                   #0
        language = 'Language'                       #1
        setting_button = 'Setting'                  #2
        home_button = 'Home Page'                   #3
        environment = 'Environment'                 #4
        detail = 'Detail'                           #5
        about = 'About'                             #6
        wlcm = 'Welcome!'                           #7
        wlcm_txt = 'Notice Board'                   #8
        setting = 'Setting'                         #9
        dt_env = 'Environment Details'              #10
        env_txt1 = 'Download Python'                #11
        env_txt2 = 'Install Environment'            #12
        env_txt3 = 'Subsoil Basic'                  #13
        env_txt4 = 'Subsoil Dev'                    #14
        apply = 'Apply'                             #15
        light = 'Light'                             #16
        sce = 'Pip Source'                          #17
        pypi = 'PyPI Source'                        #18
        tuna = 'Tsinghua Mirror'                    #19
        download = 'Download'                       #20
        install = 'Install'                         #21
        error1 = 'Detected existing Python environment'   #22
        sc = 'The library installation is complete!'      #23
        dlsc = 'The Python installation is complete!'     #24
        libn = 'Lib Name'                                 #25
        libist = 'Lib Install'                            #26
        evc = 'Checkup'                                   #27
        pynfd = 'None'                                    #28
        pyv = 'unknow vision'                             #29
        pon = 'Open file'                                 #30

        en = [
            version, language, setting_button, home_button, environment,
            detail, about, wlcm, wlcm_txt, setting, dt_env, env_txt1,
            env_txt2, env_txt3, env_txt4, apply, light, sce, pypi, tuna,
            download, install, error1, sc, dlsc, libn, libist, evc, pynfd,
            pyv, pon
        ]
        return en

    if choose == 1:
        # 中文词条
        version = '版本 0.1.2'                      #0
        language = '语言'                           #1
        setting_button = '设置'                     #2
        home_button = '主页'                        #3
        environment = '环境'                        #4
        detail = '详细'                             #5
        about = '关于'                              #6
        wlcm = '欢迎!'                              #7
        wlcm_txt = '公告栏'                         #8
        setting = '设置'                            #9
        dt_env = '环境详情'                         #10
        env_txt1 = '下载 Python'                    #11
        env_txt2 = '安装环境'                       #12
        env_txt3 = 'Subsoil 基础'                   #13
        env_txt4 = 'Subsoil 开发'                   #14
        apply = '应用'                              #15
        light = '灯泡'                             #16
        sce = 'Pip源'                              #17
        pypi = 'PyPI源'                            #18
        tuna = '清华源'                             #19
        download = '下载'                           #20
        install = '安装'                            #21
        error1 = '检测到已存在的Python环境'           #22
        sc = '库安装完成!'                           #23
        dlsc = 'Python安装完成!'                     #24
        libn = '库名'
        libist = '自定义库安装'
        evc = '环境检查'
        pynfd = '未找到'
        pyv = '未知版本'
        opn = '打开文件夹'

        zh = [
            version, language, setting_button, home_button, environment,
            detail, about, wlcm, wlcm_txt, setting, dt_env, env_txt1,
            env_txt2, env_txt3, env_txt4, apply, light, sce, pypi, tuna,
            download, install, error1, sc, dlsc, libn, libist, evc, pynfd,
            pyv, opn
        ]
        return zh