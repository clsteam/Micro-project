## Algorithms in Bioinformatics
**The programs should be flexible, i.e., it should be possible to:**

* Align sequences over any alphabet. The alphabet can be {A, C, G, T} for DNA or 

20 letters alphabet for amino acids, or any alphabet. The alphabet is specified in the 
parameter file.

* Use any score matrix. The score matrix is specified in the parameter file.

* Output the optimal alignment score and the optimal alignment.


**Detail of the programming task**

* You are required to write one program:

    
```
python3 global_align parameter.txt input.fa output.txt
```


* When you run your program, you need to limit your memory usage by

```
ulimit -Sv 250000
```

#### Dependency package

* Numpy: the fundamental package for scientific computing with Python.
* Biopython: a set of freely available tools for biological computation
* Coloredlogs: colored terminal output(You can choose not to install)


#### Usage



```
python3 global_align.py parameter.txt input.fa output.txt slope[Default:6] multi[Default:0]
```


#### Parameters

* The penalty (h) for initiating the gap should be set from 0 to a negative number in `parameter.txt`

* The penalty (s) depending on the length of the gap should be set in standard `input. slope[Default:6]`
* multi[Default:0]
0 : Only one optimal alignment (default)
1 : Output multiple optimal alignments

#### Egg

* When you run, you can set the logging setting `level='DEBUG'` to see the traceback path. 
* Because the Affine gap model backtracking process has more than one optimal path, when you set `multi=1`, the program automatically returns multiple optimal paths (the optimal score is the same).


#### Result1

* 2019-06-04 23:01:33 DESKTOP-yao GlobalAlign[18032] INFO Loading parameters
* 2019-06-04 23:01:33 DESKTOP-yao GlobalAlign[18032] INFO h: -2.0	s: 2
* 2019-06-04 23:01:33 DESKTOP-yao GlobalAlign[18032] INFO Initialization matrix
* 2019-06-04 23:01:33 DESKTOP-yao GlobalAlign[18032] INFO filling matrix of V,E,F
* 2019-06-04 23:01:33 DESKTOP-yao GlobalAlign[18032] INFO Backtracking [Multi]
* 2019-06-04 23:01:33 DESKTOP-yao GlobalAlign[18032] INFO Generate result file with detailed content
* 2019-06-04 23:01:33 DESKTOP-yao GlobalAlign[18032] INFO score = -1.0
* 2019-06-04 23:01:33 DESKTOP-yao GlobalAlign[18032] INFO S: HEAGAWGHE-E
* 2019-06-04 23:01:33 DESKTOP-yao GlobalAlign[18032] INFO T: ---PAW-HEAE
* 2019-06-04 23:01:33 DESKTOP-yao GlobalAlign[18032] INFO S: HEAGAWGHE-E
* 2019-06-04 23:01:33 DESKTOP-yao GlobalAlign[18032] INFO T: P---AW-HEAE
* 2019-06-04 23:01:33 DESKTOP-yao GlobalAlign[18032] INFO Congratulations! ^*_*^

#### Result2

<<<<<<< HEAD
* 2019-06-04 23:03:04 DESKTOP-yao GlobalAlign[18800] INFO Loading parameters
* 2019-06-04 23:03:04 DESKTOP-yao GlobalAlign[18800] INFO h: -5.0	s: 2
* 2019-06-04 23:03:04 DESKTOP-yao GlobalAlign[18800] INFO Initialization matrix
* 2019-06-04 23:03:04 DESKTOP-yao GlobalAlign[18800] INFO filling matrix of V,E,F
* 2019-06-04 23:05:23 DESKTOP-yao GlobalAlign[18800] INFO Backtracking [Multi]
* 2019-06-04 23:05:23 DESKTOP-yao GlobalAlign[18800] INFO Generate result file with detailed content
* 2019-06-04 23:05:24 DESKTOP-yao GlobalAlign[18800] INFO score = 9748.0
* 2019-06-04 23:05:24 DESKTOP-yao GlobalAlign[18800] INFO There are 192 optimal alignment paths
* 2019-06-04 23:05:24 DESKTOP-yao GlobalAlign[18800] INFO Congratulations! ^*_*^




=======
2019-06-04 23:03:04 DESKTOP-yao GlobalAlign[18800] INFO Loading parameters

2019-06-04 23:03:04 DESKTOP-yao GlobalAlign[18800] INFO h: -5.0	s: 2

2019-06-04 23:03:04 DESKTOP-yao GlobalAlign[18800] INFO Initialization matrix

2019-06-04 23:03:04 DESKTOP-yao GlobalAlign[18800] INFO filling matrix of V,E,F
2019-06-04 23:05:23 DESKTOP-yao GlobalAlign[18800] INFO Backtracking [Multi]
2019-06-04 23:05:23 DESKTOP-yao GlobalAlign[18800] INFO Generate result file with detailed content
2019-06-04 23:05:24 DESKTOP-yao GlobalAlign[18800] INFO score = None
2019-06-04 23:05:24 DESKTOP-yao GlobalAlign[18800] INFO There are 192 optimal alignment paths
2019-06-04 23:05:24 DESKTOP-yao GlobalAlign[18800] INFO Congratulations! ^*_*^
>>>>>>> 31bca41f634848c2f07402b4f52b0b3b7d320b55
