# Seida

**Seida** is a **S**ymbolic **E**xecution plugin for **IDA**.

**Seida** is C/S architecture:
* the **server** is responsible for providing the symbolic execution of the simulation environment.
* the **client** as IDA plugin.

​     

# Server

Before we can use the client-side plugin, we need to start the server first. For now we use [angr](https://github.com/angr/angr) as execution engine, we can replace it with any other engine later.

Create venv and install angr:

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install angr
```

then we can start **Seida Server** inside venv: 
```bash
$ python server.py
SEIDA_SERVER_ADDR = "http://0.0.0.0:50052"
> 
```

You also can input some simple python code in this server console(It's the same environment as the client side), e.g.:
```bash
> print(project.arch)
<Arch AARCH64 (LE)>
```

If you want write some complex code, you can write them in a script file and use `load` command to load it:
```bash
> load init_script
```

> NOTE: you also can use `python server.py init_script` to launch the server, it will auto load `init_script` at beginning. 



​                    

# Install

Before install plugin, you need to change `SEIDA_SERVER_ADDR` in `serda.py` first.

and then:
* As Script: use `File / Script file...` in IDA to load `serda.py` .
* As Plugin: change `SEIDA_USE_AS_SCRIPT` to `False`, and then put `serda.py` in the IDA/plugins folder.


​                

# Usage

When the plugin is installed, the following buttons will be added to the IDA toolbar:
* **[start]**, start symbolic simulation execution from the current position.
* **[step]**, step one instruction
* **[stepb]**, step one basic block
* **[stept]**, step to cursor position 

​             

# Command

In addition to these buttons, **Seida** also provide some python commands, you can use them in IDA's Python console.

## Load File

Before you can do anything, you need to load the file same as the current loaded by IDA.

```python
$ seida.load(filepath, base_addr=0)
```

> NOTE: If your server and client are not on the same machine, the `filepath` file is the file on the server, not on the client.

​  

## Dump Memory

```python
$ seida.dump_memory(addr, size)
7fffffffffed870  f8 ff ff ff ff ff ff ff  ff ff ff ff 00 00 00 00  |................|
7fffffffffed880  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
7fffffffffed890  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
7fffffffffed8a0  e8 ff ff ff ff ff ff ff  00 00 00 00 00 00 00 00  |................|
7fffffffffed8b0  f0 ff fe ff ff ff ff 07  4c 1b f2 00 00 00 00 00  |........L.......|
7fffffffffed8c0
```

​            

## Set Register

```python
$ seida.set_reg(reg_name, val)
```

​           

## Hook Function

```python
$ seida.hook_func(func_addr)
```

​            

## Run Script

Write a python script file:

```python
x = claripy.BVS('x', 8 * 8)  # symbolic heap memory
simulation.active[0].memory.store(0x00102c98, x, size=8)
```

> NOTE: For more information about symbolic execution, please go to [angr](https://github.com/angr/angr).


and then load this script:

```python
$ seida.do_file(py_file_path)
```


