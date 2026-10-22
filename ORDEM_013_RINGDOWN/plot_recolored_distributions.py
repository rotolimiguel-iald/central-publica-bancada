"""Plot measured simulation distributions, not significance or observed O5 data."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent

def main():
    report=json.loads((ROOT/'C5_RECOLORED_FORECAST.json').read_bytes())
    control=json.loads((ROOT/'C5_RECOLORED_VALIDATION.json').read_bytes())
    fig,axes=plt.subplots(1,2,figsize=(11,4.8),sharex=True,sharey=True)
    groups=['220_440','220_221_222_440','eight_modes']
    for ax,family in zip(axes,['SEOBNRv4HM','IMRPhenomXPHM']):
        for y,fit in enumerate(groups):
            for injected,offset,color in [(0.,.10,'#2458a6'),(1.,-.10,'#c26900')]:
                row=next(r for r in report['results'] if r['family']==family and r['psd']=='O5' and r['SNR']==40 and r['recovery']==fit and r['reading']=='R-B' and r['content']=='FULL_IMR' and r['injected_a']==injected)
                low,median,high=row['lnB']['quantiles_05_50_95']
                ax.errorbar(median,y+offset,xerr=[[median-low],[high-median]],fmt='o',color=color,capsize=4,
                    label=f'Injected a={injected:g}: median and 5–95%' if y==0 else None)
            prior=next(r for r in control['noise_only_prior_volume'] if r['family']==family and r['psd']=='O5' and r['recovery']==fit)
            ax.plot(prior['noise_only_lnB_mean'],y,'x',color='#333333',markersize=8,
                label='Noise only: mean' if y==0 else None)
        ax.axvline(0,color='#777777',linewidth=.8,linestyle='--')
        ax.set_title(family);ax.set_xlabel('ln B (reading B / GR)')
        ax.set_yticks(range(3),['220 + 440','220 + 221 + 222 + 440','Eight modes'])
        ax.set_ylim(2.5,-.5);ax.grid(axis='x',alpha=.2)
    axes[0].legend(loc='lower left',fontsize=8)
    fig.suptitle('O5 A+ design scenario • same 50 paired O4 noise intervals • network SNR 40',fontsize=12)
    fig.text(.5,.025,'True remnant fixed; proper amplitude priors. Overlapping distributions and prior-volume shifts are not detections.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.07,1,.93])
    fig.savefig(ROOT/'C5_O5_DISTRIBUTIONS.png',dpi=170)
    fig.savefig(ROOT/'C5_O5_DISTRIBUTIONS.svg')
    print(str(ROOT/'C5_O5_DISTRIBUTIONS.png'))

if __name__=='__main__':main()
