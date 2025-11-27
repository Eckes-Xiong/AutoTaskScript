"""
    # name: "edge刷积分"
    # 更新时间:2025-07-01
    # cron: 2 5,9,11,13,15,17,19,21,23 * * *
🎯 Bing Rewards 自动化脚本 - 多账号支持版-v1.0
变量名：bing_ck  多账号换行 
如果执行的发现积分不增长，且脚本上显示的积分跟实际不符，很有可能不是同一个账号的cookie，建议重新抓取。
From:yaohuo28507

363379340@qq.com  ss_123456 + H颖
"""
import requests
import random
import re
import time
import json
import os
from datetime import datetime, date, time as time_module
from urllib.parse import urlparse, parse_qs
import threading

if os.path.isfile('notify.py'):
    from notify import send

    print("加载通知服务成功！")
else:
    print("加载通知服务失败!")
# 尝试导入notify，失败则使用本地打印替代
# try:
#     import notify
# except ImportError:
#     class Notify:
#         def send(self, title, content):
#             print("\n--- [通知] ---")
#             print(f"标题: {title}")
#             print(f"内容:\n{content}")
#             print("-------------------------------")
#     notify = Notify()

def print_log(title: str, msg: str, account_index: int = None):
    """打印带时间戳的日志，支持账号编号前缀"""
    now = datetime.now().strftime("%H:%M:%S")
    if account_index is not None:
        title = f"账号{account_index} - {title}"
    print(f"{now} [{title}]: {msg or ''}")

# 从环境变量获取cookie，支持多行（一行一个）
def get_cookies(account_index=None):
    """从环境变量获取cookie，支持多行（一行一个）"""
    # env_cookies = os.getenv("bing_ck")
    env_cookies = "";
    if env_cookies:
        # 分割多行cookie，去除空行和空白字符
        cookies_list = [ck.strip() for ck in env_cookies.strip().split("\n") if ck.strip()]
        return cookies_list
    else:
        print_log("配置错误", "未配置 bing_ck 环境变量，无法执行任务", account_index)
        return []

# 获取cookie列表
# cookies_list = get_cookies()
cookies_list = ["ANON=A=70F1E69EDA4343A60E6DF6B9FFFFFFFF; _UR=QS=0&TQS=0&Pn=0; MUID=3D9C4ABE76DE667F024B5FE577B86777; MSPTC=4WnrdnBrVq9NYpdY24SOLfGdqsiCJtmvuZv3VCuJzh8; MSCCSC=1; BFBUSR=BFBHP=0; SRCHUSR=DOB=20250118&T=1743497705000&DS=1&POEX=W; fbar=imgfbar=1; imgv=lodlg=1; _tarLang=default=zh-Hans&newFeature=tonetranslation; _TTSS_OUT=hist=WyJpdCIsImVuIiwiemgtSGFucyJd; MSCC=cid=le55pnomarwpovloyegy52d4-c1=2-c2=2-c3=2; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=CA13C339D5414DF396D8C34D4DE65172&dmnchg=1; _TTSS_IN=hist=WyJmciIsIml0IiwiZW4iLCJhdXRvLWRldGVjdCJd&isADRU=0; vdp=0; _HPVN=CS=eyJQbiI6eyJDbiI6MTMyLCJTdCI6MCwiUXMiOjAsIlByb2QiOiJQIn0sIlNjIjp7IkNuIjoxMzIsIlN0IjowLCJRcyI6MCwiUHJvZCI6IkgifSwiUXoiOnsiQ24iOjEzMiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyNS0xMS0xM1QwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjo0NjgsIlRvYm4iOjB9; MicrosoftApplicationsTelemetryFirstLaunchTime=2025-11-13T09:23:36.548Z; _EDGE_S=SID=31E946A7022A614628A6500903046070; .MSA.Auth=CfDJ8BJecyNyfxpMtsfDoM3OqQtxdIha9XPXySYmrxGplJ9OoLzKqp1p2JIeBByp46HtatZrx1XbpO-aBFy6wS98D81BJZTW0Yey2I8es5BdMMfZXQoNHSx3prxbyvQjqMframrjLhSMEAGaChhokoG1MwRYwknl--2pu8ob9nvVOHGyj8PtrUBDqBW6NPUoJEVGCnf7AFqg8hef3ijcnEd70G2vdnIWjoYNiyGFVUI1C7rqDF9VS21OLeBDdki99KZgS1Jds7vTLxI1MPi-n6AJBOUihPG5yTR4meCXAZGBrizx4NnRnF9M3LEzXL-kRs-lbDP9QlWvIex7WPgYOaCRHcJZ-UjqdAqpB2946VWj9m7VfXQi0VftCFhftOUDqhIq6w; _U=1S7jF5M7NzqzCoZmXtv2nFSITnBi852zqE5vg7pmqIywK8iaNzY9LYtuQmeLNF6NhkuTW0U_YM_D2RFPP92fpcDwOABA3Znosj3v4ZGoquexfwMlqjh8sMTeDJKz0XDRBsqIs28hZTJqXU9mLYYXh5AooxbY8tlI7HiKEYnBF4eQS5aKxZJrH-gVU7CgpFJRADsyUFIHAK2ey_awVlBP_kA; WLS=C=9dddaa0f4eff91dc&N=Eckes; _Rwho=u=d&ts=2025-11-24; SNRHOP=I=&TS=; _SS=SID=31E946A7022A614628A6500903046070&PC=CNNDSE&R=2006&RB=2006&GB=0&RG=17925&RP=1998&OCID=ML2BF0; dsc=order=BingPages; _RwBf=mta=0&rc=2006&rb=2006&rg=17925&pc=1998&mtu=0&rbb=0.0&clo=0&v=1&l=2025-11-24T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=1762997017&rwflt=1763942213&rwaul2=0&g=&o=16&p=BINGCOPILOTWAITLIST&c=MY02ED&t=6990&s=2023-04-05T03:59:23.3056179+00:00&ts=2025-11-24T08:00:28.5258824+00:00&rwred=0&wls=2&wlb=0&wle=0&ccp=2&cpt=0&lka=0&lkt=0&aad=0&TH=&cid=0&gb=2025w17_c&e=V9YItrgoobTEZZvHiMWn_1YzHHQzr9m2Uj7aqR6Lah2g1FUI-r1L9PxOPBLrJ8igG-ZIEnVQS4BzxTXP7zltpw&A=70F1E69EDA4343A60E6DF6B9FFFFFFFF; USRLOC=HS=1&ELOC=LAT=30.547340393066406|LON=114.20296478271484|N=%E6%B1%89%E9%98%B3%E5%8C%BA%EF%BC%8C%E6%B9%96%E5%8C%97%E7%9C%81|ELT=2|&DLOC=LAT=30.549777|LON=114.197458|A=150|N=|C=|S=|TS=251124080029|ETS=251124081029|&BID=MjUxMTI0MTU0ODIxXzBmMjY5Yzc2M2IxNjFiNjViMTJlZTcwYTVlODhlMzUxNmY3ZjFhNmUzODgzM2JjOWQ2OGM2NTRlYWQwZGZmYzU=; SRCHHPGUSR=SRCHLANG=zh-Hans&PV=15.0.0&BZA=0&DM=1&BRW=XW&BRH=S&CW=1731&CH=382&SCW=1716&SCH=2053&DPR=1.3&UTC=480&EXLTT=31&HV=1763971225&HVE=CfDJ8BJecyNyfxpMtsfDoM3OqQv6KZ1ySEsaM1iGfjHjekxBA7e4Ys0HQrjhqyRZjBx8bqgIeUiYofFr6TkapQB_3ErQ1UR4vJ8EVv_9cg8S73xF48TKgT0NLXxC1rUWLXPuRNvTS8QmvThhDOrDafAAH6t4TvonhI6i46EMtbxYjh7jW9eGMN5uDGCmfCY95OPiFg&PRVCW=1731&PRVCH=923&AV=14&ADV=14&RB=0&MB=0&IG=98D4E774C0514F7D890A721F00E2BC89&B=0&PREFCOL=1; .AspNetCore.Antiforgery.icPscOZlg04=CfDJ8NgbImSOu2ZNnxwuqP69elCPYsJnDumpbsyDXmKTdp1150eMH1pZ_qjm2d3CN4sZVzunYgY0ngaq2VBY3Se0jZcdHUd8Tri_hHsuKywyaBQj8QtymiWzoMGbxQI9JiFmJ9vfeoTtpQ5vkRgugflv63E; GRNID=49bed262-cf4f-4fd0-8773-4a8477a79714; tifacfaatcs=CfDJ8NgbImSOu2ZNnxwuqP69elD17KKq6yUZqfyRQ9Zxrp0d_Z8FQSrCDN6GNiK4uTPFHUQTgXO22lzntNLoEGzMC8uEzltgL1c21Q2M6H1LGZ2TScv_3qP52sdw0ODaZh58jot-91vYvdpXJcVt7n16CF4mBHG_P4RM5ij9VFRqNQSovHFAZkIOErE_64BAbzU9f2s0pgEaCTi4hIRBfcTMP5GHtC3BOJDvZVaF6XvrTXRKF34Ia4IvR2VBrrz7lDirMeVDsv9cJt11TMvREI2LkBy6tDNS0aBrY0dnNQOujfQFp7FBaMH36HYFTFpDfHSqLFT6z-BwKghVM9A4snPJ1ij3QdpiLRQLJAhc-2-wN_D_LXPejUcI5OnCSfNANig6keRgNsz7nb3DcZlg3RBXecm_2I4VXJmkAWt6OTfvctS-nTqAuHpR4ft4QHH2TlWP8v0gAGS-g-lyYLYpfz4rqyibjY1K3Oy01RAwbukUGMjzHi445rCpnzD4iwdusrZkzltE5_TLFeqmcNKH_-Jq1wBnholWOPRdoobVYtgAZl22PIT-gthCF9FadG-GRqlWe8rYFm032iM3Fdf5cQuJ48paPZtCqYasONDnlO0jYEnrkg93SJbFpEYUbGagOs277HGpYy4jE81hyR8O7YqXkuMW-VDXL8DwHJcqULSm0ijirOUcNBLrxr09yWfdKRmDGjT0zNUybfAxR2V3xVXb19xnkxyKbtYntoTHEo70HvSwNnl_f1509VBXtAAWMOexqdNlxdbk6X86uLSbJ9eMq2yr1ryQsgOEi6fpz1abu3SreoKHzqhx7P4-pRuoIm2EhVCh_ixa2S2EUSFbFUmA6ToSo-aOUHxrcryu-_GmkzCVH_XswZxXMv6FV5mt0lrOgE2rhMm1t1Wyp65rMTUzXolpBck8DjhEwppebGtYh0eTwOAZ-Pq3IQOMHIGUm_L6GADX44xLAfdtXsv-yuJU2fBUi3D-s7wTP3FUf1gkNEQk9fGeN7W_r9dGuyo-Za_vDcqHWzfqdhRJ--VWaeE-bVM1kqWjE5ZPlcS1D4dadrbTmCBxy6t6eexI_UGcrump2e9kNW5mXMfqXajlOKQJxrG1oIvXsNN2KvW13PaePhdsbnNrHk7G13C5X_wbeUJAxbExZy5xhyROQVgvpPc7NvG830T8id9q7A0-GJb-oNKv1GhCKkXMk8GJoggWB1eEyQL8MR7E03u-Uirv4F1oI0jruCLTyf7MAeIx8wkvKvxM0P9UwjkY2hBjQXJRY-VzQW1HTH67_1GigHCWzIcFfJeD7bWifdn5jDxEQKIJkDt7uClJsXkC_l3zZIk4pCA-z93F7ddTMRgm-X0zUKXu2W0AyMFK5c59QkD49ThAEnuTwYLuSwjpDdorSytTfUELVmOMBw-ymUFNz0KN9wfHB4TAYpSKeqC3fZ_sHYMjuz0Q3kZJYlvP1g71un9j87kJpDekHw5ON4XO9LQCb5btLqnRWlAX2srAsOdf1YHSs3Ed38UJ6fthvIAKXBedJOMzbrb9eRCuf5oZTvi_-OZlhDCUY33YdOw9Xvp3qR303crPj6dznRIBsF35XSorpRYbf86FEdRV2DZl_yCVyXXq44tVrcVY-IvgqnlkZO-5yJwlHJzkwlyNca8cqusDxhr37sGwuCF-kz1fXx8vRVucB42U18lEiPwXtm8D2YQYr_LKk8du_1qsv-JGuilb2PuZbbKHFqAA6f0BSyDhP6_soi-kLcv2PebD7rzom8j_yOsfOXKl18ATlgC2-9bjlD3wnrvEopwstICC93rbzAuePuu2WzQ93P1UuhgO56VVVDUteO4DneUtnHQpcZjAnQWLtXqBNAe4qXJNLOAbcdT7s6RO5uXsJ_qlgLJ-uxF1iYjglLmtPbdauNx7GR8ts_nDWy7s0rNtxtoVRc6jjSOwQKZtaxUSMExlHZb13fPtjhw51fxm2iDf35ppM37xTEBQ-bwCoa8w5aGJXfn8uS9n8zfrNW-r9KNP6ioZu1fRjkfQEQQZlHi-5klFJvzV0zTHIKc-nV11jYYuwXILh0MJ3capHZHkLDZlavUxpPKDfX9ZoybDY3FQPMytZSdKGmf5mD8Pj85zaqhbaaHXCwxs68iZOi-iH9vl2K7Dz6IWVb708csj5FBikyx8fRs0JUDzcs5UgTCUjx3bVPHW9oElZWc-pgSsjcf5dpKFqnpG10J-DsQAOXAI-AAi-gzgi5bBJZb_3EGBx5Kpnb0Jaxva1mMBFyoWab7BlY6_qvJ3HwnjaJeQ9PH2-WlQKfLX3ny5B24Qb_cWafObemI0ZykObchFdw2pqDLCmnpBvDOOgVks3KS74--_fSrkM7ebQNYJ43-Q5zHNPHJel6-coWOmvsAM0RN0QTLj3mfbiKa-99mheCgq6vD40YblIkGxwiOIrNjhjyLQbCnDXsA4OLtRA7gqTWzh_mW3Ms7oxlzaOskjA5w7DSf_2tOgY7GBaEf30-P08PV-M4JBJTKDx-MuvQ4R848LHAtbSAxL_jRqATi4vuezZfdNYgIexQP9A6NqsTmMO2qtT7PGPLmED_NJ2Le8Z9MHd0M5nCTzNPG_PCbJJ02Q26kPimIPdIOxZ2hPnKUc0yzxXLp8GZBUHlFQ47gLuHv32I4NanTkWeY0lV78c-R40pwH0xodpMg9-Kg3m8W36DnbluwFvU7nCMEB8VeyYtPW5xKfdDBehVr_5XdK83WZDSZQDK-n9J2heXgvlQLWQvd-UoZxiey0fkpo58buXrqTW81E5Zz7ZFg6TNqPQEJhOBQpAPf6b6VMtkVtX5bj6UvLEJXKiLCU4P59P7Xc35mr4LXmaoSnq9MZHOJxHtfszFDioZCK5F2IM2SGEKLoJdf5WlGeoRS48Ceurt9nooTCXea7a44AOb_2Sm8cKZ2Aw8BKfdjlv1yhbNpp9b8iJ_10xLvcVOQa2DU-gr2-orkbpXMkWEcL1PbuF_UvHv05b4gMjtdgRZrOMegUsOGS3BbqsykgsXwRqtUta9og3erHX9-cK-rpI-3Q6YVEzz2Gk7xFTMSqztOilug3Z3kNjp4fWwVfcLQOHwfGMYQq0-9l-qlVtJW5k4C3bfmA8mRT1PtIkSOxPmRvkbTQyKDb8Nc0LvbbahFHISTylh0yCHD9_7G_SNVcnIF-7wTuXH0mXARE2Pzuf-H1Z4F-82F-tFJDiLY8A004sOSddWCPmj_jnOIiYr1GfVFA569p0eHGh7NXcsfKPRz42QnR-We8xEbbAuShL80Cn1hA6RVNGDiLJjrqNAZQclbeK1d9GMax76Nvd_MNO1ydktquJe0lzzjdYmRCzb2BI-l73XOapPEJnfm3jsbV7Nmkd9DNrwaBnwV54-7A_Asq_PlW_WIuINpuDR6ww-QuYgKH0c5i0H9PkDcugoPOTCbVIU-g-LtQJsxWkjNg4styRhnNEa0GvPOoCfUYfxzvTRnjiCKdRUroEXrklCiX6abPqgrykc4JpWaI_cEkhKHHie_pNOp1FkV0Eu-AQGCCmFZNDbT68hqTeysZ0jYj71FjZthSBdeyEp2e7bKH3uNJtQwKHcYA_PbAraTyOng5cVkypbaSm5PR7z-TkCGh6cAdUlpooCJaI1BylagmFYQVo95cg518lvVFvpbDNT0ACElBjBVEePMH44mPnlpUMFOZ2jwqwE-SxJ2oq4Ry0c7z2AFIc72yBzIE_H9uj83kWTv6QTA0DX7n8tOQSDetSFjymUc4MbKSDSdfHwq7gl9VAd66t2WLxkuNeEhFUnDODhI1dbII2FSMrDAVGYiITj5bgchzRDgbGoRooXT6vTlfVneZ1Dd5Wy9IAe21VfkDYJHMSIJhcaF5YoklXr7B51DsvdGe; _C_Auth=; _C_ETH=1; GC=PL7qzkMbIlV2qNsJVWDnSjTlcQpm3C_aHVCIvUwrevnkPtYpTzH11ZM01S9le57W5QDXlTXs-60dXSaF3hl3Bg; webisession=%7B%22impressionId%22%3A%22ef6d2c94-9df2-4ce3-b3da-14c77dcebda7%22%2C%22sessionid%22%3A%2234dfb468-a037-4a29-a64d-4472cea78039%22%2C%22sessionNumber%22%3A3%7D", "MUID=05CDC25A7F80640A0377D7357EAE65C5; _EDGE_V=1; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=D8ACE0C230444EE0828480E82B6495AF&dmnchg=1; MUIDB=05CDC25A7F80640A0377D7357EAE65C5; _UR=QS=0&TQS=0&Pn=0; MicrosoftApplicationsTelemetryDeviceId=b9ed43e2-ffba-4449-a617-0eeaeb3d927f; MicrosoftApplicationsTelemetryFirstLaunchTime=2025-07-08T10:08:55.964Z; MSCC=cid=516ei9y25yz1rs3to5sx8emb-c1=2-c2=2-c3=2; MSPTC=gzbQBpCWcbB_GTU48A1FLmiqW33AwnE8c2KOMBlVNu4; BFBUSR=BFBHP=0; ANON=A=E107A683AD39B3CC3C53D2BCFFFFFFFF; USRLOC=HS=1&ELOC=LAT=30.545801162719727|LON=114.19879150390625|N=%E6%B1%89%E9%98%B3%E5%8C%BA%EF%BC%8C%E6%B9%96%E5%8C%97%E7%9C%81|ELT=4|; vdp=0; _EDGE_S=SID=34ECCF04FE3A63C33BE7D9AAFF7962B7; ipv6=hit=1763975208993&t=4; _RwBf=r=0&ilt=3&ihpd=1&ispd=0&rc=16083&rb=16083&gb=2025w28_c&rg=0&pc=14506&mtu=0&rbb=0.0&g=&cid=0&clo=0&v=1&l=2025-11-24T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=1762539049&rwflt=1762539028&rwaul2=0&o=16&p=search_and_earn&c=ML2W7B&t=3208&s=2025-07-08T10:12:47.3633810+00:00&ts=2025-11-24T08:06:53.5352787+00:00&rwred=0&wls=0&wlb=0&wle=1&ccp=2&cpt=0&lka=0&lkt=0&aad=0&TH=&mta=0&e=eAitne2l_ySzTgWxOWGLsv5pnT3n1FvRhVWj5r_8GOfDDwQhnYD4UmA27oBj8qcdupJWrmrO5uTN0Xmw5gUikA&A=; _Rwho=u=d&ts=2025-11-24; _SS=SID=34ECCF04FE3A63C33BE7D9AAFF7962B7&R=16083&RB=16083&GB=0&RG=0&RP=14506; _C_Auth=; GRNID=e37f6362-e16e-4267-8a31-7535d0523f17; _U=1yKWwhkJUQshY5P5mU1qR9iQ2eXGpky8RW3qYU_6iip7PydN61FKTLtK6NCVOOZCkb-UmAr00-dUNojGtICIS7fpq_HEkJlznXs1bJ_8QO_XqTfdMY_uxvw3mzKj9DTEuTXua24pYhnMJmxBje0ZSBJBOiXSY9d9lun7a_aY68zwFFvcZYttW_YyIfoo8qfAXuK3tATjP-3LFfzUdulDtV9Odkrie1cECOLeUL4lPoz0; WLS=C=2547924acd0a9cd2&N=%e9%a2%96; SRCHUSR=DOB=20250109&T=1736405119000&TPC=1736405119000&DS=1&POEX=W; _HPVN=CS=eyJQbiI6eyJDbiI6MjQsIlN0IjowLCJRcyI6MCwiUHJvZCI6IlAifSwiU2MiOnsiQ24iOjI0LCJTdCI6MCwiUXMiOjAsIlByb2QiOiJIIn0sIlF6Ijp7IkNuIjoyNCwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyNS0xMS0yNFQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjo1NCwiVG9ibiI6MH0=; SRCHHPGUSR=SRCHLANG=zh-Hans&BZA=0&HV=1763971609&DM=1&BRW=XW&BRH=S&CW=1486&CH=330&SCW=1471&SCH=330&DPR=1.3&UTC=480&PV=15.0.0&WTS=63872001920&PRVCW=1485&PRVCH=742&EXLTT=4&HVE=CfDJ8BJecyNyfxpMtsfDoM3OqQv9wM9IPAxEhmu2kY8HjbjzLGQV4b0a_e2ru7z9KmIpP_txlapEQQ507kIZFBdwv_cVXDS1A4N3sXspKudstXgJtPoX8jsLW5VeJDG0suI3UMsPXZjxdSpAMecL3A2pD5ZXFr3ZH9wejWH-hbcZuYHAtE8yUMmXSzAtaJSofImN2w&PREFCOL=1&IG=EFCFED00E60E4B7981A047A5A2A6BFB6&B=0; tifacfaatcs=CfDJ8NgbImSOu2ZNnxwuqP69elCLgQtsOoaYOKVc6oZj4KHVFHrzrFI1CGKmVz5ChgJAIbE0vCNYNEoMKijdL5QgtbY3dE8Ncl7EcAivxhs4w4np_-3BFrkUsUf_-XIsc04NzFZ91YTLhHYHdTCe4vO_9IyDW0C8wV86eV_vl3wrnpBN3Jm-1rBtuedR50k9DOY1H1VZJZI6eLoz_IQzMrJ6wkkcm9MIfI8fgLFQHV2F1SAt5Cyo9b1-GXIhZasYPULHpU-451Yyg3I5yLnfDASvCVT7LUPT3d9WbbS8p_TdJE-fDiPesf06eNDDbANAMBJyT-pkkMoJVqlee3YmOcd8S1s7V6N_mh809tH9HxpgdCouwyn4tdeg1e1TMLuzE3lEGaIEDQ0oGq1yItHji2_KeMUhoDTDemValQ0Lh7CFgdg3mOTHYI1F1lwXE90smXhKHe6vsgHzPDTm_aq2Ccp63K7YurSLpbLSQvXnj5gi-5DLZmoAYAZDlG1dhvf2MPijIvMzy_16J1JTPyATtKsVHaf3FPoRhqvuOirgN32O1YZE6TtYECK4f7FxmRLjVlalp3e8q4a0FCeQndgS-cu7FNBSVM-hHVl1KkO2j8P3rlgmL1eU48HlvE-vEJXuXw9p3oXzC3ssnHQMn2uQi0SJcDIKJ9gWR06CqVN7zkMrDIJjJRFmS5bycOhbDpH769lFnuas7qZl1d3uZPGGfo-zb6Gn_-aenLWY9ahH6lFHfVYIXNHQqiHgwBK3HoXpJqfpvAKb02LpxPNemtKR6t7RIg1IyzLStBvjIEy5uBMdDWrcc4C4Hbgci1XhLQO8lLT_m0ReyKSqxcJ7D6xxcwsLhMbMaso_yFzN2j45XgZx_YRFaH3lin6aL9Un46UtucScM-9aL18c9tp1837lf4xTu6hRuIkQob_FWD8RmatVg6oTjaIabvrscDR1KGTGK_L23cjMIgVK3_nCSNWlUSbJGzh8uU5vmlwIKx024lbnmU2O-02qO-Xc_dpIfBY64zyZ6fPWz-cUdfGU1tP48B5sapwMaE2Idj9uxweLATRBeYedblttJM__JKSdJl7jbF6IbYQ6M2r910xqaf_OIjECUh1WH-JUWOJGXaYT_6N1rmLLsaV3YD4X9-_Xz5_Wj1vWS04UBE34fDgu2dkMh09ghG3cOuAw9tWUf-U3QVm0X1eu0KLz34Qx1p_0_sssGnJyc6si6I3WL8Ve9xmisn5wBp0B4cr4JF5g9Pu5v8SZE_41JmKOQhpXzhjVe_4yUNLuyDS2gxBzIMcdynU8yjcr2Y4mIfqjWfRd0Pqqq0Qg_JN7yvNREMRDehceiEUy7ApXdTrjgKXXaThwXbQAVelcup6TG3hx_-FjWDABjf0YKUiLv-lP0V_Cdmso2CCRzeJxJRqTdVg73NePAE_tqVZYvyzAR_dVGKQ6Z9tv5XJEiRxiKnRaVhjeGKmdEYibY8X34Q2MbL_MzBqyX4qBVfWCOGepTC60yVQUEF9DgUrtlI2tDLj86gqurlTvcsb-urbWzFlP4CEcA-3AiPE8srrX4RwVfBnYshzQZthv6nhtaQM8BPB3J--9xDxdx076AQ4n3pbRwjEW5_JItJEYiX5Kl-tU2Jk2ZQ07V4u_ve-7au6Ge_S8CMRoiplVw6t4UPi7HlR8Ws8CtYx8CQBYH0jROc-kGZluVjHjHSFE0Xs62I8hLXAiWrqE2Lm0m1bhE2eA9rBf5Jjq_yOePUTK9UnOQhNG9lHwPrDcXSVF_JaDXdKex28i_nJoIbZ06P72d2YZE8rTjeAQ1fanC3HPBAePThTnRrru6W45bfpUtG_P-xmSY651ULSbtUHj1TFYPlVxkpjn_Rl1IkVIHZi-9qv0CdZ_xeSYsrAA8Cj0N7UGrbAQuyLWyvITjvnKZTE1N-QAY44EGzf3WyAGAhCSz_AMzYTYiAHbQGbkHng2PaASnrVzuERl0o7BrltW2ixOxeIu6pMZq6cMiaeY0vb3na5j2mu9azXP7MzBiX8ZGHyRNe23iftinHExDN2z3Oc-7lVBjBDu8LHQASrddqLBVfTeY1mOr1dggUCbBDTBLryT-E9g-2_9M7ZbWMiLLXrQVE8e7bMyiy6BdgM3xvjyYBUNQcGIrR8Z1OnXWDtoMQOfj2bcH92CgwmSrho5uOounNtBBVzmo8aC0jhRLDiwRoTGBwcZg4xzhrRfT__f5-cpakhBDabYMKDu6B_BoaOlGekmMWMOE3Nhy8RcaEbvV0sV_ou54jFmbqIX6RyK-hyBMCvxKqrEAKADQVzkZkz6kLVOYHhr-jq8geVUXn-Tih9Mkls4j_nfXFPo2iW_G7z48UgA2ferfuOmxL8ouYBUIFI99X8zVNCESBSVXPQRHt6LcARah6PBglHeFk0RVGLgdwtVl-8sOfwrEIvSgODFgr2CLOk9ruk8ki45zTozVi41Jk1mZolTfICvMbSp6eLC9p14G5fT79CXGqRqVZsff85xf7lVY6DdkjojFi35jvdeXIlfujtOPDUKoNTIOkd_rvq4sbYeYUpTeD0FnXE0zzE1geOffNpKj1ThvbfMw1xDzEVPZ_Tb6P6c9n1KxjIET1aFI6Y2BH5nA7uR7te62O2DfMAhRw9nkftGVVaUPlMYl67lFvU_iqefX2ds9bUvS6pVb7jKRWBZwGBZ9-Bs9_u7GkKqhjyUxaOogjrvpEG6TP2d1jUdYYhLbpkA3s59Dh-Kmtnq9c62vxoajbexP8h3dws3ncIITYVNuCMvK9M6Ud2MRPgdeTe-0jG_TkLM3Q0xk3Tpq42WuUTxN7-U0DNZKgmm6SCHrfXS61VLMLcftiDvcoRgAMs2Vz16S-97OOyNXG3U1iVd2XgR_QK9mPPi9oAogKIM2nPux1SdVSVyCLOu2XVwr-ufwGiPqCU_zXPVaiQpo0cAT1V_-CBEWvmDSb5Rj9xPeRgWkISEJAta1nHHhURU_dfJC0V9KtDKVaQXPcpdAorGoJzSp4p85VcHEF0t4V10v-Gs8O0y1YWzn8n-jM6JPRb2PUqyPjPRaakWIGF_9MIdwEAgyBCH1DIQruJqlRFA3jc-Q6OqprP-2v8zg35WXTKO4JwX2Gi53u8_18h5pvvnXcBwUTwJUp5CTJ5RYjeo2z4UUMvZ9uINMcr9syvw2lCj-JioCnoFgPIromnqsnrAM_pZiNQ1LFpjbaV0-8-K75R8Yki_4ahUVt4Dcq2gQINLfuFNPvEypdiU-rouTcPoy4eIhpwo3nG_sARNDMdBMHf0XG-wAzh0Lxsqcm_DYyT8kwPJRhG5wA7V6HIWjPBwCdjIGBIPF4AtMSMm7tjf2E0LVjNWuUwpsOMHS_l56ybXwhxT1-9zTlPdB6pkBradCAgyl5WVqe0kPduCRm65KmwBNglLDilbofeJxFDneMWheqQNOglmZpfcjfmIchqHajgQd9f42YlCwFwK2P8VHGKq8-SMtDwHMZYHW49ul1U_Lw4mnaKWkujjRz83sIMhYQ6Dcadz3zLeWA20i9Z_SDtdqsKoOvvnJklIXQcip-Y3y2OUG2ynHoPie6MsCoohsPlhN3TJt6kV5MQEwjVFEm5F-uJzn7ty0fDlCiYuuLpEGfg6KMo1eUXfcDeupnx4iDX0Z3dIrSrjod_bLEE66fpIv2YJ8Z9NYbcL60crKAzMJnWNC8_ZATgS4CA8ofGL1zeK-FcmpIXHjcQz0Orv4LgHNKX_OTi4U5Hjbhu0e2tgY7EFAdbXyVM6oQ9g13kc7rWp3yDCyvYK0AYI_H9eCLcODLloQRL-mnyLLvo13SMhyk6Pu9cQ36S_0r22kWysmv-IE2HjaxClDKvgcXvu-v9t2QcgKLzd32M37KAthCviftMkBWIh5ykE; .AspNetCore.Antiforgery.icPscOZlg04=CfDJ8NgbImSOu2ZNnxwuqP69elCht4oTeUzA0xnCbJDp29oz2LU0Bmnn-kMe9X88CP8slRHvXIPvb1TO4E1g8MUaFgJxORwzu4oZpfhDan8YCsG65ecUcYYy3PdtNmX_GEZBzq3MokxVnjESLUnlCS1KH6Y; _uetsid=a22d79c0c90c11f0956885b273f4d2c8; _uetvid=1c9b13f05be411f0a2f1e11cab84f371; _clck=1ac26k1%5E2%5Eg1a%5E1%5E2015; _clsk=1tr9a6w%5E1763971656240%5E1%5E0%5Ei.clarity.ms%2Fcollect; _C_ETH=1; webisession=%7B%22impressionId%22%3A%229bd1e91b-03a6-438e-ad49-b77949fd12cc%22%2C%22sessionid%22%3A%22991b8415-e552-4abf-b6bb-22e01b563b55%22%2C%22sessionNumber%22%3A3%7D"]
if not cookies_list:
    print_log("启动错误", "没有可用的cookie，程序退出", None)
    exit(1)

print_log("初始化", f"检测到 {len(cookies_list)} 个账号，即将开始...", None)

# 浏览器通用头部（将在运行时根据当前cookie动态设置）
BROWSER_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "referer": "https://rewards.bing.com/"
}

# 新增：热搜词API及默认词库
HOT_WORDS_APIS = [
    ("https://dailyapi.eray.cc/", ["weibo", "douyin", "baidu", "toutiao", "thepaper", "qq-news", "netease-news", "zhihu"]),
    ("https://hot.baiwumm.com/api/", ["weibo", "douyin", "baidu", "toutiao", "thepaper", "qq", "netease", "zhihu"]),
    ("https://cnxiaobai.com/DailyHotApi/", ["weibo", "douyin", "baidu", "toutiao", "thepaper", "qq-news", "netease-news", "zhihu"]),
    ("https://hotapi.zhusun.top/", ["weibo", "douyin", "baidu", "toutiao", "thepaper", "qq-news", "netease-news", "zhihu"]),
    ("https://api-hot.imsyy.top/", ["weibo", "douyin", "baidu", "toutiao", "thepaper", "qq-news", "netease-news", "zhihu"]),
    ("https://hotapi.nntool.cc/", ["weibo", "douyin", "baidu", "toutiao", "thepaper", "qq-news", "netease-news", "zhihu"]),
]
DEFAULT_HOT_WORDS = [
    "盛年不重来，一日难再晨", "千里之行，始于足下", "少年易学老难成，一寸光阴不可轻", "敏而好学，不耻下问", "海内存知已，天涯若比邻", "三人行，必有我师焉",
    "莫愁前路无知已，天下谁人不识君", "人生贵相知，何用金与钱", "天生我材必有用", "海纳百川有容乃大；壁立千仞无欲则刚", "穷则独善其身，达则兼济天下", "读书破万卷，下笔如有神",
    "学而不思则罔，思而不学则殆", "一年之计在于春，一日之计在于晨", "莫等闲，白了少年头，空悲切", "少壮不努力，老大徒伤悲", "一寸光阴一寸金，寸金难买寸光阴", "近朱者赤，近墨者黑",
    "吾生也有涯，而知也无涯", "纸上得来终觉浅，绝知此事要躬行", "学无止境", "己所不欲，勿施于人", "天将降大任于斯人也", "鞠躬尽瘁，死而后已", "书到用时方恨少", "天下兴亡，匹夫有责",
    "人无远虑，必有近忧", "为中华之崛起而读书", "一日无书，百事荒废", "岂能尽如人意，但求无愧我心"
]

# 只保留推送相关的 load_used_words 和 save_used_words
USED_WORDS_FILE = "Bing_Rewards_Cache.json"
used_words_lock = threading.Lock()

def load_used_words():
    if not os.path.exists(USED_WORDS_FILE):
        return {}
    try:
        with open(USED_WORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_used_words(data):
    today = date.today().isoformat()
    keys_to_keep = []
    for k in data:
        date_part = None
        if '_' in k:
            date_part = k.split('_')[-1]
        elif k.startswith('push_'):
            date_part = k.replace('push_', '')
        if date_part and date_part >= today:
            keys_to_keep.append(k)
    new_data = {k: data[k] for k in keys_to_keep}
    with open(USED_WORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

# fetch_hot_words 和 get_next_hot_word 只做热搜词的获取和随机，不再写入/读取used_words文件

def fetch_hot_words(max_count=30):
    """base_url和sources都随机顺序，依次全部尝试，只要有一个source成功获取热搜词就立即返回，全部失败用默认词库"""
    apis_shuffled = HOT_WORDS_APIS[:]
    random.shuffle(apis_shuffled)
    for base_url, sources in apis_shuffled:
        sources_shuffled = sources[:]
        random.shuffle(sources_shuffled)
        for source in sources_shuffled:
            api_url = base_url + source
            try:
                resp = requests.get(api_url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, dict) and 'data' in data and data['data']:
                        all_titles = [item.get('title') for item in data['data'] if item.get('title')]
                        if all_titles:
                            print_log("热搜词", f"成功获取热搜词 {len(all_titles)} 条，来源: {api_url}")
                            random.shuffle(all_titles)  # 打乱顺序
                            return all_titles[:max_count]
            except Exception:
                pass
    print_log("热搜词", "全部热搜API失效，使用默认搜索词。")
    default_words = DEFAULT_HOT_WORDS[:max_count]
    random.shuffle(default_words)
    return default_words

hot_words = fetch_hot_words()

def get_next_hot_word(account_index=None, email=None):
    """每次随机返回一个热搜词"""
    return random.choice(hot_words) if hot_words else random.choice(DEFAULT_HOT_WORDS)

def get_rewards_points(cookies, account_index=None):
    """查询当前积分和账号信息"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; OPPO R11 Plus Build/PKQ1.190414.001; ) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 BingSapphire/31.4.2110003555',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'X-Search-Location': 'lat=19.3516,long=110.1012,re=-1.0000,disp=%20',
        'Sapphire-OSVersion': '9',
        'Sapphire-Configuration': 'Production',
        'Sapphire-APIVersion': '114',
        'Sapphire-Market': 'zh-CN',
        'X-Search-ClientId': '2E2936301F8D6BFD3225203D1E5F6A0D',
        'Sapphire-DeviceType': 'OPPO R11 Plus',
        'X-Requested-With': 'com.microsoft.bing',
        'Cookie': cookies
    }

    url = 'https://rewards.bing.com/'
    params = {
        'ssp': '1',
        'safesearch': 'moderate',
        'setlang': 'zh-hans',
        'cc': 'CN',
        'ensearch': '0',
        'PC': 'SANSAAND'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        content = response.text
        
        # 提取积分
        points_pattern = r'"availablePoints":\s*(\d+)'
        points_match = re.search(points_pattern, content)
        
        # 提取邮箱账号
        email_pattern = r'email:\s*"([^"]+)"'
        email_match = re.search(email_pattern, content)
        
        available_points = None
        email = None
        
        if points_match:
            available_points = int(points_match.group(1))
            # print_log("积分查询", f"当前积分: {available_points}")
        else:
            print_log("积分查询", "未找到 availablePoints 值", account_index)
            
        if email_match:
            email = email_match.group(1)
            # print_log("账号信息", f"账号: {email}")
        else:
            print_log("账号信息", "未找到 email 值", account_index)
            
        return {
            'points': available_points,
            'email': email
        }
            
    except requests.exceptions.RequestException as e:
        print_log("积分查询", f"请求失败: {e}", account_index)
        return None
    except Exception as e:
        print_log("积分查询", f"发生错误: {e}", account_index)
        return None

def bing_search_pc(cookies, account_index=None, email=None):
    # 使用热搜词
    q = get_next_hot_word(account_index, email)
    #print_log("搜索关键词", f"本次搜索词: {q}", account_index)

    url = "https://cn.bing.com/search"
    params = {
        "q": q,
        "qs": "PN",
        "form": "TSFLBL"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": "https://rewards.bing.com/",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": cookies
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print_log("电脑搜索", f"电脑搜索异常: {e}", account_index)
        return False

def bing_search_mobile(cookies, account_index=None, email=None):
    """执行移动设备搜索，使用热搜词"""
    q = get_next_hot_word(account_index, email)
    #print_log("搜索关键词", f"本次搜索词: {q}", account_index)

    # 模拟真实移动搜索请求的cookie
    enhanced_cookies = cookies
    
    # 移除桌面版特有的cookie字段，这些可能影响移动搜索识别
    import re
    
    # 移除桌面版特有的字段
    desktop_fields_to_remove = [
        r'_HPVN=[^;]+',
        r'_RwBf=[^;]+', 
        r'_U=[^;]+',
        r'USRLOC=[^;]+',
        r'BFBUSR=[^;]+',
        r'_Rwho=[^;]+',
        r'ipv6=[^;]+',
        r'_clck=[^;]+',
        r'_clsk=[^;]+',
        r'webisession=[^;]+',
        r'MicrosoftApplicationsTelemetryDeviceId=[^;]+',
        r'MicrosoftApplicationsTelemetryFirstLaunchTime=[^;]+',
        r'MSPTC=[^;]+',
        r'vdp=[^;]+'
    ]
    
    for pattern in desktop_fields_to_remove:
        enhanced_cookies = re.sub(pattern, '', enhanced_cookies)
    
    # 清理多余的分号和空格
    enhanced_cookies = re.sub(r';;+', ';', enhanced_cookies)
    enhanced_cookies = enhanced_cookies.strip('; ')
    
    # 替换SRCHUSR为简化版本（移除DS和POEX参数）
    if 'SRCHUSR=' in enhanced_cookies:
        enhanced_cookies = re.sub(r'SRCHUSR=[^;]+', 'SRCHUSR=DOB=20250706', enhanced_cookies)
    else:
        enhanced_cookies += '; SRCHUSR=DOB=20250706'
    
    # 确保有SRCHD字段
    if 'SRCHD=' not in enhanced_cookies:
        enhanced_cookies += '; SRCHD=AF=NOFORM'
    
    # 添加或替换SRCHHPGUSR为移动设备版本
    if 'SRCHHPGUSR=' in enhanced_cookies:
        enhanced_cookies = re.sub(r'SRCHHPGUSR=[^;]+', 'SRCHHPGUSR=SRCHLANG=zh-Hans&DM=0&CW=360&CH=493&SCW=360&SCH=493&BRW=MM&BRH=MS&DPR=3.0&UTC=480&PR=3&OR=0&PRVCW=360&PRVCH=493&HV=1751764054&HVE=CfDJ8Inh5QCoSQBNls38F2rbEpSFNIuT7R7A-dN544maOpoSyIiAlvCb43wPmzrMB8xLZeNzPTVPZYSpNz07pdIhrHpXIpf7BsQSxPNmP9esnrCjcj4OTSnzlqIQ0NroSiLt3Awrdp6qCqmkbZUfleTej6Bio11sryZznjdagVAUt5JoBZSzj5SbjYNHGoSgrIu2Ow&PREFCOL=0', enhanced_cookies)
    else:
        enhanced_cookies += '; SRCHHPGUSR=SRCHLANG=zh-Hans&DM=0&CW=360&CH=493&SCW=360&SCH=493&BRW=MM&BRH=MS&DPR=3.0&UTC=480&PR=3&OR=0&PRVCW=360&PRVCH=493&HV=1751764054&HVE=CfDJ8Inh5QCoSQBNls38F2rbEpSFNIuT7R7A-dN544maOpoSyIiAlvCb43wPmzrMB8xLZeNzPTVPZYSpNz07pdIhrHpXIpf7BsQSxPNmP9esnrCjcj4OTSnzlqIQ0NroSiLt3Awrdp6qCqmkbZUfleTej6Bio11sryZznjdagVAUt5JoBZSzj5SbjYNHGoSgrIu2Ow&PREFCOL=0'

    url = "https://cn.bing.com/search"
    params = {
        "q": q,
        "form": "NPII01",
        "filters": "tnTID:\"DSBOS_F29F59C848FA467D96D2F8EEC96FBC7A\" tnVersion:\"8908b7744161474e8812c12c507ece49\" Segment:\"popularnow.carousel\" tnCol:\"39\" tnScenario:\"TrendingTopicsAPI\" tnOrder:\"ef45722b-8213-4953-9c44-57e0dde6ac78\"",
        "ssp": "1",
        "safesearch": "moderate",
        "setlang": "zh-hans",
        "cc": "CN",
        "ensearch": "0",
        "PC": "SANSAAND"
    }

    headers = {
        "host": "cn.bing.com",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 9; OPPO R11 Plus Build/PKQ1.190414.001; ) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 BingSapphire/31.4.2110003555",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "x-search-location": "lat=19.3516,long=110.1012,re=-1.0000,disp=%20",
        "sapphire-osversion": "9",
        "sapphire-configuration": "Production",
        "sapphire-apiversion": "114",
        "sapphire-market": "zh-CN",
        "x-search-clientid": "2E2936301F8D6BFD3225203D1E5F6A0D",
        "sapphire-devicetype": "OPPO R11 Plus",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": enhanced_cookies,
        "x-requested-with": "com.microsoft.bing"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print_log("移动搜索", f"移动设备搜索异常: {e}", account_index)
        return False



def get_dashboard_data(cookies, account_index=None):
    """统一获取dashboard数据和token"""
    try:
        headers = {
            **BROWSER_HEADERS,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "cookie": cookies
        }
        resp = requests.get("https://rewards.bing.com/", headers=headers, timeout=30)
        resp.raise_for_status()
        
        html_text = resp.text
        token_match = re.search(r'name="__RequestVerificationToken".*?value="([^"]+)"', html_text)
        dashboard_match = re.search(r'var dashboard\s*=\s*(\{.*?\});', html_text, re.DOTALL)
        
        if not token_match:
            print_log('Dashboard错误', "未能获取 __RequestVerificationToken", account_index)
            return None
        
        if not dashboard_match:
            print_log('Dashboard错误', "未能获取 dashboard 数据", account_index)
            return None
        
        token = token_match.group(1)
        dashboard_json = json.loads(dashboard_match.group(1).rstrip().rstrip(';'))
        
        return {
            'dashboard_data': dashboard_json,
            'token': token
        }
    except Exception as e:
        print_log('Dashboard错误', str(e), account_index)
        return None

def complete_daily_set_tasks(cookies, account_index=None):
    """完成每日活动任务"""
    # print_log('每日活动', '--- 开始检查网页端每日活动 ---')
    completed_count = 0
    try:
        # 获取dashboard数据
        dashboard_result = get_dashboard_data(cookies, account_index)
        if not dashboard_result:
            return completed_count
        
        dashboard_data = dashboard_result['dashboard_data']
        token = dashboard_result['token']
        
        # 提取积分信息
        if 'userStatus' in dashboard_data:
            user_status = dashboard_data['userStatus']
            available_points = user_status.get('availablePoints', 0)
            lifetime_points = user_status.get('lifetimePoints', 0)
            # print_log("每日活动", f"? 当前积分: {available_points}, 总积分: {lifetime_points}", account_index)
        
        # 提取每日任务
        today_str = date.today().strftime('%m/%d/%Y')
        daily_tasks = dashboard_data.get('dailySetPromotions', {}).get(today_str, [])
        
        if not daily_tasks:
            print_log("每日活动", "没有找到今日的每日活动任务", account_index)
            return completed_count
        
        # 过滤未完成的任务
        incomplete_tasks = [task for task in daily_tasks if not task.get('complete')]
        
        if not incomplete_tasks:
            # print_log("每日活动", "所有每日活动任务已完成", account_index)
            return completed_count
        
        print_log("每日活动", f"找到 {len(incomplete_tasks)} 个未完成的每日活动任务", account_index)
        
        # 执行任务
        for i, task in enumerate(incomplete_tasks, 1):
            print_log("每日活动", f"执行任务 {i}/{len(incomplete_tasks)}: {task.get('title', '未知任务')}", account_index)
            
            if execute_task(task, token, cookies, account_index):
                completed_count += 1
                print_log("每日活动", f"? 任务完成: {task.get('title', '未知任务')}", account_index)
            else:
                print_log("每日活动", f"? 任务失败: {task.get('title', '未知任务')}", account_index)
            
            # 随机延迟
            time.sleep(random.uniform(2, 4))
        
        print_log("每日活动", f"每日活动执行完成，成功完成 {completed_count} 个任务", account_index)
        
    except Exception as e:
        print_log('每日活动出错', f"异常: {e}", account_index)
    
    return completed_count

def setup_task_headers(cookies):
    """设置任务执行的请求头"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Ch-Ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Ch-Ua-Platform-Version': '"19.0.0"',
        'Sec-Ch-Ua-Model': '""',
        'Sec-Ch-Ua-Bitness': '"64"',
        'Sec-Ch-Prefers-Color-Scheme': 'light',
        'Sec-Ms-Gec': '1',
        'Sec-Ms-Gec-Version': '1-137.0.3296.83',
        'Cookie': cookies
    }
    return headers

def setup_api_headers(cookies):
    """设置API请求的请求头"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://rewards.bing.com',
        'Referer': 'https://rewards.bing.com/',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Ch-Ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Ch-Ua-Platform-Version': '"19.0.0"',
        'Sec-Ch-Ua-Model': '""',
        'Sec-Ch-Ua-Bitness': '"64"',
        'Sec-Ch-Prefers-Color-Scheme': 'light',
        'Sec-Ms-Gec': '1',
        'Sec-Ms-Gec-Version': '1-137.0.3296.83',
        'Cookie': cookies
    }
    return headers

def extract_tasks(more_promotions):
    """提取任务"""
    tasks = []
    for promotion in more_promotions:
        complete = promotion.get('complete')
        priority = promotion.get('priority')
        attributes = promotion.get('attributes', {})
        is_unlocked = attributes.get('is_unlocked')
        # 只要complete为False且(priority为0或7，或is_unlocked为True)
        if (complete == False or complete == 'False') and (
            priority == 0 or priority == 7 or is_unlocked is True or is_unlocked == 'True'):
            tasks.append(promotion)
    return tasks

def extract_search_query(destination_url):
    """从URL中提取搜索查询"""
    try:
        parsed_url = urlparse(destination_url)
        query_params = parse_qs(parsed_url.query)
        if 'q' in query_params:
            search_query = query_params['q'][0]
            import urllib.parse
            search_query = urllib.parse.unquote(search_query)
            return search_query
        return None
    except Exception as e:
        print_log("更多活动", f"提取搜索查询失败: {e}", None)
        return None

def report_activity(task, token, cookies, account_index=None):
    """报告任务活动，真正完成任务"""
    if not token:
        return False
    
    try:
        post_url = 'https://rewards.bing.com/api/reportactivity?X-Requested-With=XMLHttpRequest'
        post_headers = setup_api_headers(cookies)
        payload = f"id={task.get('offerId', task.get('name'))}&hash={task.get('hash', '')}&timeZone=480&activityAmount=1&dbs=0&form=&type=&__RequestVerificationToken={token}"
        response = requests.post(post_url, data=payload, headers=post_headers, timeout=15)
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get("activity") and result["activity"].get("points", 0) > 0:
                    print_log("更多活动", f"? 获得{result['activity']['points']}积分", account_index)
                    return True
                else:
                    return False
            except json.JSONDecodeError:
                return False
        else:
            return False
    except Exception as e:
        return False

def execute_task(task, token, cookies, account_index=None):
    """执行单个任务"""
    try:
        destination_url = task.get('destinationUrl') or task.get('attributes', {}).get('destination')
        if not destination_url:
            print_log("更多活动", f"? 任务 {task.get('name')} 没有目标URL", account_index)
            return False
        
        # 检查是否为搜索任务
        search_query = extract_search_query(destination_url)
        
        if search_query:
            # 搜索任务
            print_log("更多活动", f"? 执行搜索任务: {task.get('title')}", account_index)
        else:
            # 非搜索任务（如Edge相关任务）
            print_log("更多活动", f"? 执行URL访问任务: {task.get('title')}", account_index)
            
            # 对于Edge相关任务，可能需要特殊处理URL
            if 'microsoftedgewelcome.microsoft.com' in destination_url:
                # 转换为实际的Microsoft URL
                if 'focus=privacy' in destination_url:
                    destination_url = 'https://www.microsoft.com/zh-cn/edge/welcome?exp=e155&form=ML23ZX&focus=privacy&cs=2175697442'
                elif 'focus=performance' in destination_url:
                    destination_url = 'https://www.microsoft.com/zh-cn/edge/welcome?exp=e155&form=ML23ZX&focus=performance&cs=2175697442'
        
        # 设置任务执行请求头
        headers = setup_task_headers(cookies)
        
        # 发送请求
        response = requests.get(
            destination_url, 
            headers=headers, 
            timeout=15,
            allow_redirects=True
        )
        
        if response.status_code == 200:
            print_log("更多活动", f"? 任务执行成功", account_index)
            # 报告活动
            if report_activity(task, token, cookies, account_index):
                return True
            else:
                print_log("更多活动", f"?? 任务执行成功但活动报告失败", account_index)
                return False
        else:
            print_log("更多活动", f"? 任务执行失败，状态码: {response.status_code}", account_index)
            return False
            
    except Exception as e:
        print_log("更多活动", f"? 执行任务时出错: {e}", account_index)
        return False

def complete_more_activities(cookies, account_index=None):
    """完成更多活动任务"""
    # print_log('更多活动', '--- 开始检查更多活动 ---')
    completed_count = 0
    
    try:
        # 获取dashboard数据
        dashboard_result = get_dashboard_data(cookies, account_index)
        if not dashboard_result:
            print_log("更多活动", "无法获取dashboard数据，跳过更多活动\n", account_index)
            return completed_count
        
        dashboard_data = dashboard_result['dashboard_data']
        token = dashboard_result['token']
        
        # 提取积分信息
        if 'userStatus' in dashboard_data:
            user_status = dashboard_data['userStatus']
            available_points = user_status.get('availablePoints', 0)
            lifetime_points = user_status.get('lifetimePoints', 0)
            # print_log("更多活动", f"? 当前积分: {available_points}, 总积分: {lifetime_points}", account_index)
        
        # 提取更多活动任务
        more_promotions = dashboard_data.get('morePromotions', [])
        tasks = extract_tasks(more_promotions)
        
        if not tasks:
            # print_log("更多活动", "没有找到可执行的更多活动任务", account_index)
            return completed_count
        
        print_log("更多活动", f"找到 {len(tasks)} 个可执行的更多活动任务", account_index)
        
        # 执行任务
        for i, task in enumerate(tasks, 1):
            print_log("更多活动", f"执行任务 {i}/{len(tasks)}: {task.get('title', '未知任务')}", account_index)
            
            if execute_task(task, token, cookies, account_index):
                completed_count += 1
            else:
                print_log("更多活动", f"? 任务失败: {task.get('title', '未知任务')}", account_index)
            
            # 随机延迟
            time.sleep(random.uniform(2, 4))
        
        print_log("更多活动", f"更多活动执行完成，成功完成 {completed_count} 个任务\n", account_index)
        
    except Exception as e:
        print_log('更多活动出错', f"异常: {e}\n", account_index)
    
    return completed_count

search_thread_stopped = threading.Event()

def get_search_progress_sum(dashboard_data, search_type):
    user_status = dashboard_data.get('userStatus', {})
    counters = user_status.get('counters', {})
    search_tasks = counters.get(search_type, [])
    return sum(task.get('pointProgress', 0) for task in search_tasks)

def perform_search_tasks(search_type, search_func, cookies, account_index=None):
    check_interval = 2 if search_type == "电脑搜索" else 1
    print_log(search_type, f"{search_type} - 执行{check_interval}次搜索 ---", account_index)
    count = 0
    dashboard_result = get_dashboard_data(cookies, account_index)
    dashboard_data = dashboard_result['dashboard_data'] if dashboard_result and 'dashboard_data' in dashboard_result else None
    progress_type = 'pcSearch' if '电脑' in search_type else 'mobileSearch'
    last_progress = get_search_progress_sum(dashboard_data, progress_type) if dashboard_data else 0
    for i in range(check_interval):
        count += 1
        if search_func(cookies, account_index):
            delay = random.randint(20, 50)
            print_log(search_type, f"第 {count} 次{search_type}成功，等待 {delay} 秒...", account_index)
            time.sleep(delay)
        else:
            print_log(search_type, f"第 {count} 次{search_type}失败", account_index)
        # 每次都检查进度
        dashboard_result = get_dashboard_data(cookies, account_index)
        dashboard_data = dashboard_result['dashboard_data'] if dashboard_result and 'dashboard_data' in dashboard_result else None
        current_progress = get_search_progress_sum(dashboard_data, progress_type) if dashboard_data else last_progress
        # 第check_interval次搜索完成后输出进度变化
        if count == check_interval:
            print_log(f"{search_type}", f"已完成{count} 次，进度变化: {last_progress} -> {current_progress}", account_index)
        # 检查任务是否完成
        if progress_type == 'pcSearch':
            if is_pc_search_complete(dashboard_data):
                print_log(f"{search_type}", f"电脑搜索任务已完成", account_index)
                break
        elif progress_type == 'mobileSearch':
            if is_mobile_search_complete(dashboard_data):
                print_log(f"{search_type}", f"移动搜索任务已完成", account_index)
                break
    # check_interval次后统一中止线程
    # if not ((progress_type == 'pcSearch' and is_pc_search_complete(dashboard_data)) or (progress_type == 'mobileSearch' and is_mobile_search_complete(dashboard_data))):
    #     print_log(f"{search_type}", f"{check_interval}次后任务未完成，停止线程", account_index)
    #     search_thread_stopped.set()
    #     raise SystemExit()

def is_pc_search_complete(dashboard_data):
    for task in dashboard_data['userStatus']['counters'].get('pcSearch', []):
        if not task.get('complete', True):
            return False
    return True

def is_mobile_search_complete(dashboard_data):
    for task in dashboard_data['userStatus']['counters'].get('mobileSearch', []):
        if not task.get('complete', True):
            return False
    return True

def get_cached_init_points(email, date_str):
    key = f"init_{email}_{date_str}"
    data = load_used_words()
    entry = data.get(key)
    if entry and str(entry.get("init_points")) != "None":
        return entry["init_points"]
    return None

def set_cached_init_points(email, date_str, points):
    try:
        data = load_used_words()
        key = f"init_{email}_{date_str}"
        if key in data and str(data[key].get("init_points")) != "None":
            return
        data[key] = {
            "init_points": points,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_used_words(data)
    except Exception:
        pass

def format_account_summary(dashboard_data, email, script_start_points, final_points, account_index=None):
    prefix = f"账号{account_index} - " if account_index is not None else "账号: "
    lines = [f"{prefix}{email}"]
    lines.append(f"?积分变化: {script_start_points} -> {final_points} (+{final_points - script_start_points})")
    # 搜索任务
    user_status = dashboard_data.get('userStatus', {})
    counters = user_status.get('counters', {})
    for search_type, label in [("pcSearch", "电脑搜索"), ("mobileSearch", "移动搜索")]:
        search_tasks = counters.get(search_type, [])
        for task in search_tasks:
            title = task.get('title', label)
            progress = f"{task.get('pointProgress', 0)}/{task.get('pointProgressMax', 0)}"
            lines.append(f"?{label}: {progress}")
    # 每日活动
    lines.append("?---------- 每日活动 ----------")
    today_str = date.today().strftime('%m/%d/%Y')
    daily_tasks = dashboard_data.get('dailySetPromotions', {}).get(today_str, [])
    if daily_tasks:
        for task in daily_tasks:
            title = task.get('title', '每日任务')
            complete = '?' if task.get('complete') else '?'
            lines.append(f"{complete}{title}: {'已完成' if task.get('complete') else '未完成'}")
    else:
        lines.append("无每日活动任务")
    # 更多活动
    lines.append("?---------- 更多活动 ----------")
    more_tasks = dashboard_data.get('morePromotions', [])
    if more_tasks:
        for task in more_tasks:
            # 只显示pointProgressMax或activityProgressMax大于0的任务
            ppm = task.get('pointProgressMax', 0) or 0
            if ppm > 0:
                title = task.get('title', '更多任务')
                complete = '?' if task.get('complete') else '?'
                lines.append(f"{complete}{title}: {'已完成' if task.get('complete') else '未完成'}")
    else:
        lines.append("无更多活动任务")
    return '\n'.join(lines)

def single_account_main(cookies, account_index):
    """单个账号的完整任务流程"""
    #print(f"\n{'='*15} [开始处理账号 {account_index}] {'='*15}")
    
    # 1. 查询初始积分和账号信息（重试3次）
    #print_log("账号信息", "---查询账号信息和初始积分 ---", account_index)
    initial_data = None
    for retry in range(3):
        initial_data = get_rewards_points(cookies, account_index)
        if initial_data is not None and initial_data['points'] is not None:
            break
        if retry < 2:  # 前两次失败时重试
            print_log("账号信息", f"第{retry + 1}次获取失败，{3 - retry - 1}秒后重试...", account_index)
            time.sleep(3 - retry - 1)  # 递减延迟：2秒、1秒
    
    if initial_data is None or initial_data['points'] is None:
        print_log("账号信息", "重试3次后仍无法获取初始积分，跳过此账号", account_index)
        return None
    
    email = initial_data.get('email', '未知邮箱')
    today_str = date.today().isoformat()
    # 优先从缓存读取初始积分
    cached_init_points = get_cached_init_points(email, today_str)
    if cached_init_points is not None:
        script_start_points = cached_init_points
    else:
        script_start_points = initial_data['points']
        set_cached_init_points(email, today_str, script_start_points)
    print_log("账号信息", f"账号: {email}, 初始积分: {script_start_points}", account_index)
    
    # 任务前dashboard_data不再用于推送
    dashboard_result = get_dashboard_data(cookies, account_index)
    dashboard_data = dashboard_result['dashboard_data'] if dashboard_result and 'dashboard_data' in dashboard_result else None
    
    complete_daily_set_tasks(cookies, account_index)
    print_log("每日活动", "【每日活动 - 已完成】", account_index)
    complete_more_activities(cookies, account_index)
    print_log("更多活动", "【更多活动 - 已完成】", account_index)

    if dashboard_data and not is_pc_search_complete(dashboard_data):
        perform_search_tasks("电脑搜索", lambda c, ai: bing_search_pc(c, ai, email), cookies, account_index)
    else:
        print_log("电脑搜索", "【电脑搜索 - 已完成】", account_index)
    pc_completed_points = get_rewards_points(cookies, account_index)
    mobile_start_points = pc_completed_points['points'] if pc_completed_points else script_start_points
    if dashboard_data and not is_mobile_search_complete(dashboard_data):
        perform_search_tasks("移动搜索", lambda c, ai: bing_search_mobile(c, ai, email), cookies, account_index)
    else:
        print_log("移动搜索", "【移动搜索 - 已完成】", account_index)
    final_data = get_rewards_points(cookies, account_index)
    # 重新获取最新dashboard_data用于推送
    dashboard_result = get_dashboard_data(cookies, account_index)
    dashboard_data = dashboard_result['dashboard_data'] if dashboard_result and 'dashboard_data' in dashboard_result else None
    if final_data and final_data['points'] is not None:
        final_points = final_data['points']
        points_earned = final_points - script_start_points
        print_log("脚本完成", f"? 最终积分：{final_points}（+{points_earned}）", account_index)
        if dashboard_data:
            summary = format_account_summary(dashboard_data, email, script_start_points, final_points, account_index)
        else:
            summary = f"账号{account_index} ： {email}\n(未获取到dashboard数据)"
        return summary
    else:
        print_log("脚本完成", "无法获取最终积分", account_index)
        return None

def has_pushed_today():
    today = date.today().isoformat()
    used_words_data = load_used_words()
    return used_words_data.get(f"push_{today}", False)

def mark_pushed_today():
    today = date.today().isoformat()
    used_words_data = load_used_words()
    used_words_data[f"push_{today}"] = True
    save_used_words(used_words_data)

def main():
    """主函数 - 支持多账号并发执行和推送"""
    all_summaries = []
    threads = []
    summaries_lock = threading.Lock()

    def thread_worker(cookies, i):
        try:
            summary = single_account_main(cookies, i)
            if summary:
                with summaries_lock:
                    all_summaries.append(summary)
        except Exception as e:
            print_log(f"账号{i}错误", f"处理账号时发生异常: {e}", i)

    for i, cookies in enumerate(cookies_list, 1):
        t = threading.Thread(target=thread_worker, args=(cookies, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # --- 统一推送 ---
    print(f"\n\n{'='*10} [全部任务完成] {'='*10}")
    if search_thread_stopped.is_set():
        # send("未完成", "搜索任务未完成，线程被终止，取消推送。")
        print_log("统一推送", "搜索任务未完成，线程被终止，取消推送。", None)
        return
    if has_pushed_today():
        # send("今天已推过", "今天已经推送过，取消本次推送。")
        current_time = datetime.now().time();
        target_time = time_module(22, 0, 0)  
        if current_time >= target_time:
            title = f"Rewards成功({date.today().strftime('%Y-%m-%d')})"
            content = "\n\n".join(all_summaries)
            send(title, content)
            print_log("推送成功", "总结报告已发送。", None)
            mark_pushed_today()
        else:
            print_log("统一推送", "今天已经推送过，取消本次推送。", None)
        return
    if all_summaries:
        print_log("统一推送", "准备发送所有账号的总结报告...", None)
        try:
            title = f"Rewards成功({date.today().strftime('%Y-%m-%d')})"
            content = "\n\n".join(all_summaries)
            send(title, content)
            print_log("推送成功", "总结报告已发送。", None)
            mark_pushed_today()
        except Exception as e:
            print_log("推送失败", f"发送总结报告时出错: {e}", None)
    else:
        print_log("统一推送", "没有可供推送的账号信息。", None)

if __name__ == "__main__":
    main() 