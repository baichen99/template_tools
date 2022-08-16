# Useful tools for matdata

## Setup

```shell
git clone github.com/template_tools
cd template_tools
pip install requests xmindparser pytrans
```

## Examples

### Upload xml

```python
# upload_xml.py
from template_tools.src.upload import upload_xml


upload_xml('path/to/file.xml', '测试数据', team_name='测试组', template_name='测试模板')
```

### Upload zip

If you have a folder that contains `data.xml` and some attachment files, like this:

```
- zip_folder
| - data.xml
| - x.png
| - x.jpg
```

You can just use `upload_zip` to compress this folder to zip file and upload it.

```python
# upload_zip.py
from template_tools.src.upload import upload_zip

# if set compress arg to False, it means you already have zip file
upload_zip('path/to/zip_folder', '测试数据', team_name='测试组', template_name='测试模板', compress=True)
```

### Upload xmls/zips in a simple way

When you have a folder of xmls, you can use `upload_job` to upload xmls, but in this way, you cannot custom data's name, by default the format of name is `[template_name]_[index]`

```python
# upload_xml.py
from template_tools.src.upload import upload_job


upload_job(type='xml', team_name='测试组', template_name='测试模板', file_path='xmls')
```

Same to zips:

```python
# upload_zip.py
from template_tools.src.upload import upload_job


upload_job(type='zip', team_name='测试组', template_name='测试模板', file_path='zips')
```

### Delete data of template

Suppose you want to delete the data of 高温陶瓷 template under 陶瓷涂层 team and the data name starts with '高温'

```python
from template_tools.src.delete import delete_all

def filter_callback(data_list):
    return [record for record in data_list if record['name'].startswith('高温')]

delete_all('陶瓷涂层', '高温陶瓷', filter_callback)
```

### Download data to folder

Basically the same as deleting data of template

```python
from template_tools.src.download import download_all_xmls

download_all_xmls('陶瓷涂层', '高温陶瓷', output_dir='xmls')
```

### convert xmind to template.json

First, create a xmind file like `example.xmind`:

![](https://raw.githubusercontent.com/baichen99/pics/master/img/Screen%20Shot%202022-06-09%20at%2010.44.42.png)

```python
from template_tools.src.xmind2template import getTemplate

getTemplate('exmaple.xmind', dest='template.json')
```

![](https://raw.githubusercontent.com/baichen99/pics/master/img/Screen%20Shot%202022-06-09%20at%2010.46.09.png)

Then, select '上传模板' --> '本地上传' upload `template.json` to matdata editor, and you can create this template.
