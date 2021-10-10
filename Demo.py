import json

import pandas
import requests
from lxml import etree
import re


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/85.0.4183.48 Safari/537.36 Edg/85.0.564.23'}

def get_page(URL, page_index):
    res = requests.get(URL,headers=header)
    print(res)
    selector = etree.HTML(res.text)
    result = selector.xpath('//script[@type="text/javascript"]/text()')
    js_str = re.search('\{.*}', str(result[0]))
    js_dict = json.loads(js_str.group())
    job = js_dict['engine_jds']

    dict_job = {}
    job_name = []
    company_name = []
    workarea_text = []
    providesalary_text = []
    requirements = []
    companytype_text = []
    companysize_text = []
    companyind_text = []

    for i in range(len(job)):
        if 'job_name' in job[i].keys():
            job_name.append(job[i]['job_name'])
        if 'company_name' in job[i].keys():
            company_name.append(job[i]['company_name'])
        if 'workarea_text' in job[i].keys():
            workarea_text.append(job[i]['workarea_text'])
        if 'providesalary_text' in job[i].keys():
            providesalary_text.append(job[i]['providesalary_text'])
        if 'attribute_text' in job[i].keys():
            attribute_text = job[i]['attribute_text']
            requirements.append(attribute_text[1:-1])  # 经验，学历要求
        if 'companytype_text' in job[i].keys():
            companytype_text.append(job[i]['companytype_text'])
        if 'companysize_text' in job[i].keys():
            companysize_text.append(job[i]['companysize_text'])
        if 'companyind_text' in job[i].keys():
            companyind_text.append(job[i]['companyind_text'])
        else:
            companyind_text.append('')


    dict_job['name'] = job_name
    dict_job['company'] = company_name
    dict_job['work_area'] = workarea_text
    dict_job['salary'] = providesalary_text
    dict_job['requirements'] = requirements
    dict_job['company_type'] = companytype_text
    dict_job['company_size'] = companysize_text
    dict_job['field'] = companyind_text

    df = pandas.DataFrame(dict_job)

    if page_index == 1:
        df.to_csv('./Java.csv',index=None, header=True,encoding='utf_8_sig')
    else:
        df.to_csv('./Java.csv',mode='a',index=None,header=False,encoding='utf_8_sig')

if __name__ == '__main__':
    for p in range(1,200):
        url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,java,2,{}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='.format(p)
        print(p)
        get_page(url,p)