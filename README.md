# Seida

**Seida** is a **S**ymbolic **E**xecution plugin for **IDA**.

Seida is C/S architecture:
* the **server** is responsible for providing the symbolic execution of the simulation environment.
* the **client** as IDA plugin.

​     

# Server

Before we can use the client-side plugin, we need to start the server first:

```bash
$ python seida_server.py
Seida server listen on 0.0.0.0:50051
```

and change `SEIDA_SERVER_ADDR` in `serda.py`.

​                    

# Install

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

In addition to these buttons, Seida also provide some python commands, You can use them in IDA's Python console.

## Dump memory

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

## Set register

```python
$ seida.set_reg(reg_name, val)
```

​           

## Hook function

```python
$ seida.hook_func(func_addr)
```

​            

## Run any script

Write a python script:

```python
x = claripy.BVS('x', 8 * 8)
simulation.active[0].memory.store(0x00102c98, x1_mem, size=8)
```

and load this script:

```python
$ seida.do_file(py_file_path)
```


