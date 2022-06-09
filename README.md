# Useful data uploading tools for matdata

## Usage

```shell
    pip install requests xmindparser pytrans
```

## APIs

- `delete.get_all_data(template_name, team_id, token, num=1000)`

    get all data of template

- `delete.delete_all(team_id, template_name, token)`

    delete all data of template

- `upload.upload_asset(file_obj, token)`

    upload file, return relative url of file

- `upload.upload_xml(file_path, name, template_id, team_id, token)`

    add file by uploading xml file

- `upload.get_token(username, password)`

    get JWT token
  
- `upload.get_records_num(team_id, template_id, token)`

    get records' number of template

- `xmind2template.getTemplate(xmind_path, dest='template.json')`

    convert xmind file to template that can be used in matdata editor, the xmind file must be created by xmind zen or xmind 8.

## Examples

### delete all data of template

You have to get team_id, template_name manually:

Press F12, and click '录入' --> '验证' to add a data record, and you can see teamId, templateEditionId in add requests payload.

![](https://raw.githubusercontent.com/baichen99/pics/master/img/Screen%20Shot%202022-06-09%20at%2010.52.32.png)

```python
from delete import delete_all
from upload import get_token

username = 'xxx'
password = 'xxx'

token = get_token(username, password)

delete_all(team_id, template_name, token)

```

### convert xmind to template.json

First, create a xmind file like `example.xmind`:

![](https://raw.githubusercontent.com/baichen99/pics/master/img/Screen%20Shot%202022-06-09%20at%2010.44.42.png)

```python
from xmind2template import getTemplate

getTemplate('exmaple.xmind', dest='template.json')
```
![](https://raw.githubusercontent.com/baichen99/pics/master/img/Screen%20Shot%202022-06-09%20at%2010.46.09.png)

Then, select '上传模板' --> '本地上传' upload `template.json` to matdata editor, and you can create this template.