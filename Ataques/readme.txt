Ataque as redes salvas em um arquivo txt

para ler:

largest_cc = numpy.loadtxt('nomedoarquivo ou caminho do arquivo')
transitivity_ = numpy.loadtxt('nomedoarquivo')

largest_cc(..): representa o maior componente conexo da rede após uma remoção de 10 nós por iteração. Seja essa 
    remocação direciada a nós com maior número de ligações ou remoção a nós aleatórios 

transitivity_(..): representa uma métrica de centralidade, seu valor após a remoção de 10 nós por iteração, também, para
    ataques direcionado e aleatório.


