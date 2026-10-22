"""Preserve the cited zerojet engine and create its Y-derivative generalization."""
from pathlib import Path
import hashlib

def main():
    root=Path(__file__).resolve().parent
    source=root/'labelled_nonminimal_metric_euler.py'
    text=source.read_text('utf-8')
    substitutions={
      'def mixed_ward(order, nu, c, d, xword=()):':'def mixed_ward(order, nu, c, d, xword=(), yword=()):',
      "(b,nu,c,d),xword+(a,),())":"(b,nu,c,d),xword+(a,),yword)",
      "(a,b,c,d),xword+(nu,),())":"(a,b,c,d),xword+(nu,),yword)",
      "(j,d),xword,(c,))":"(j,d),xword,yword+(c,))",
      "(j,c),xword,(d,))":"(j,c),xword,yword+(d,))",
      'def cstar_mixed(order, ind):':'def cstar_mixed(order, ind, yword=()):',
      'mixed_ward(order,b,c,d,(a,))':'mixed_ward(order,b,c,d,(a,),yword)',
      'mixed_ward(order,a,c,d,(b,))':'mixed_ward(order,a,c,d,(b,),yword)',
      'mixed_ward(order-m,j,c,d,(i,))':'mixed_ward(order-m,j,c,d,(i,),yword)',
      'def euler(order, ind):':'def euler(order, ind, yword=()):',
      "M.euler('metric',order,ind)":"M.euler('metric',order,ind,yword)",
      "M.euler('metric',order-m,(i,j,c,d))":"M.euler('metric',order-m,(i,j,c,d),yword)",
      'cstar_mixed(order,ind)':'cstar_mixed(order,ind,yword)',
      'cstar_mixed(0,ind)':'cstar_mixed(0,ind,yword)',
      'def pair_contact(ind1, kind2, ind2, xword2=(), yword2=(), order=1):':'def pair_contact(ind1, kind2, ind2, xword2=(), yword1=(), yword2=(), order=1):',
      'euler(j,ind1)':'euler(j,ind1,yword1)',
    }
    for a,b in substitutions.items():
        assert text.count(a)==1,(a,text.count(a))
        text=text.replace(a,b)
    text='# Generalizes cited predecessor SHA256 '+hashlib.sha256(source.read_bytes()).hexdigest()+'\n'+text
    target=root/'labelled_nonminimal_metric_euler_v2.py';assert not target.exists()
    temp=target.with_suffix('.tmp');assert not temp.exists()
    b=text.encode();temp.write_bytes(b);assert temp.read_bytes()==b;temp.replace(target)

if __name__=='__main__':main()
