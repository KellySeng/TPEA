# TPEA Projet

Scrabblos : Jeu de mots sous la forme d’une blockchain

## Students :
* Seng Kelly
* Gerday Nathan
* Sreng David

# Requirements:
* python 3
* module pynacl
* opam 2 (for server)
* ocaml 4.08.0 (for server)

# Installation

Install Python 3 :
```
sudo apt install python3
```
Install python module pynacl :
```
sudo apt install python3-pip
pip3 install pynacl
```
Install server :
```
opam pin add scrabblos https://gitlab.com/julien.t/projet-p6.git
opam update
opam upgrade
opam install scrabblos
```

# How to use

Launch server
```
scrabblos-server -port 12345 -no-turn
```
It's important to use "-no-turn" flag because it won't work well with turns
*******
Launch authors and politicians
```
(./launch.sh <addr> <port> <dictionary> <number authors> <number politicians>)
./launch.sh localhost 12345 dict/dict_100000_5_15.txt 10 3
```
It's not memory friendly, be careful to not launch too many authors and politicians (15 authors and 5 politicians crashed my PC).

Authors and Politicians make their jobs and print the scores at the end
