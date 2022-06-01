# Python NamedTemporaryFiel 权限错误

```
  PermissionError

  [Errno 13] Permission denied: 'C:\\Users\\MAG\\AppData\\Local\\Temp\\tmpr_hxncqv'

  at ~\.pyenv\pyenv-win\versions\3.10.0\lib\pathlib.py:1117 in open
      1113│         the built-in open() function does.
      1114│         """
      1115│         if "b" not in mode:
      1116│             encoding = io.text_encoding(encoding)
    → 1117│         return self._accessor.open(self, mode, buffering, encoding, errors,
      1118│                                    newline)
      1119│
      1120│     def read_bytes(self):
      1121│
nox > Command poetry export --dev --format=requirements.txt '--output=C:\Users\MAG\AppData\Local\Temp\tmpr_hxncqv' failed with exit code 1
nox > Session tests-3.10 failed.
```

在使用nox时，需要使用 poetry 导出开发依赖到临时文件，用于nox安装所需依赖。在 **windows** 环境下报文件权限错误



## 具体问题

因为**windows**下临时文件默认创建时就打开的，打开之后再关闭临时文件会被删除，而**Linux** 可以再次打开。具体阅读python官方文档

## 解决方案

```python
def install_with_poetry(session: Session, *args: str) -> None:
    requirements = tempfile.NamedTemporaryFile(mode="w", delete=False)
    try:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("-r", requirements.name)
        session.install(*args)
    finally:
        requirements.close()
        os.remove(requirements.name)
```

使用 delete=False 设置为不删除文件，而是使用完毕后手动清除



这里如果其中使用一下方式安装依赖的话，还用另外一个坑，解决办法就是上面的编写方式，大家遇到了之后可以参考

```python
session.install(f"--constraint={requirements.name}", *args, **kwargs)
```
