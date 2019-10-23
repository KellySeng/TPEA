# TPEA Projet

Scrabblos : Jeu de mots sous la forme d’une blockchain

## Student :
* Seng Kelly
* Gerday Nathan
* Sreng David

# Installation

Install Python 3 :
```
sudo apt install python3
```
Install pip3 : 
```
sudo apt install python3-pip
```
Install python module Crypto : 
```
pip3 install pynacl
```
Install server :
```
opam pin add scrabblos https://gitlab.com/julien.t/projet-p6.git
opam update
opam upgrade
opam install scrabblos
```
Launch server
```
scrabblos-server [-bind addr] [-port 12345] [-no-turn] [-no-check-sigs]
```

