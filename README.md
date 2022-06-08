# Useful data uploading tools for matdata

## Usage

```shell
    pip install requests xmindparser pytrans
```

## APIs

- `delete.get_all_data(url, template_name, team_id, token, num=1000)`

    get all data of template

- `delete.delete_all(url, team_id, template_name, token)`

    delete all data of template

- `upload.upload_asset(file_obj, token)`

    upload file, return relative url of file

- `upload.upload_xml(file_path, name, template_id, team_id, token)`

    add file by uploading xml file

- `upload.get_token(username, password)`

    get JWT token
  
- `upload.get_records_num(team_id, template_id, token)`

    get records' number of template

- `xmind2template.getTemplate(path)`

    convert xmind file to template that can be used in matdata editor
