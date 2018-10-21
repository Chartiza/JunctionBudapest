from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from website.models import Snp

def parsedb():
    db_allele = {}
    db_coeff = {}
    gclist = {}
    links = {}
    db=list(Snp.objects.values())
    # print (db)
    for dbline in db:
    #db=list(Snp.objects.filter(snp=test_snp).values())[0]
        db_snp=str(dbline['snp'])
        links[db_snp]=str(dbline['link'])
        c=str(dbline['cancertype_id'])
        if c not in gclist:
            gclist[c]=[db_snp]
        else:
            gclist[c].append(db_snp)
        #gclist[db_snp]=gc
        db_allele[db_snp]=dbline['rareall']
        db_coeff[db_snp]=dbline['coeff']
    return gclist,db_allele,db_coeff,links

def parseFile(f,gclist,db_allele,db_coeff):
    results = {}
    for line in f:
        data=line.decode('utf-8').rstrip().split(',')
        test_snp=data[0]
        test_allele=data[-1]
        if test_snp in db_allele:
            results[test_snp]=0
            if test_allele==db_allele[test_snp]:
                results[test_snp]+=2*float(db_coeff[test_snp])
            elif test_allele[0]!=test_allele[1]:
                results[test_snp]+=1.5*float(db_coeff[test_snp])
            else:
                results[test_snp]+=1
    for c in gclist:
        for s in gclist[c]:
            if s in results:
                if c not in results:
                    results[c]=results[s]
                else:
                    results[c]+=results[s]
        if c=='1':
            results[c]=float(results[c])/(54.4)
        else:
            results[c]=float(results[c])/(44.06)
    return results

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            gclist, db_allele, db_coeff, links = parsedb()
            results = parseFile(f, gclist, db_allele, db_coeff)
            request.session['results'] = results
            return HttpResponseRedirect('results')
    else:
        form = UploadFileForm()
    return render(request, 'website/index.html', {'form': form})

def colorClassifier(value):
    if value < 0.4:
        return 'bg-success'
    elif value < 0.7:
        return 'bg-warning'
    else:
        return 'bg-danger'

def results(request):
    res = request.session['results']
    lungCancerRisk = round(res['1'], 2)
    lungCancerRiskPercents = lungCancerRisk * 100
    lungCancerRiskPercentsColor = colorClassifier(lungCancerRisk)
    breastCancerRisk = round(res['2'], 2)
    breastCancerRiskPercents = breastCancerRisk * 100
    breastCancerRiskPercentsColor = colorClassifier(breastCancerRisk)

    res.pop('1')
    res.pop('2')
    lungTableLines = []
    breastTableLines = []

    for s in res:
        snip = list(Snp.objects.filter(snp=s).values())[0]
        if s in res:
            snip1 = str(res[s])
        else:
            snip1 = '0'
        if snip['cancertype_id'] == 1:
            shortlink = snip['link'][12:]
            #lungTableLines.append([s, snip['value'], snip['link'], shortlink])
            lungTableLines.append([s, snip1, snip['link'], shortlink])
        if snip['cancertype_id'] == 2:
            shortlink = snip['link'][12:]
            #breastTableLines.append([s, snip['value'], snip['link'], shortlink])
            breastTableLines.append([s, snip1, snip['link'], shortlink])

    return render(request, 'website/results.html', 
        {
            'lungCancerRisk': lungCancerRisk,
            'lungCancerRiskPercents': lungCancerRiskPercents,
            'lungCancerRiskPercentsColor': lungCancerRiskPercentsColor,
            'lungTableLines': lungTableLines,
            'breastCancerRisk': breastCancerRisk,
            'breastCancerRiskPercents': breastCancerRiskPercents,
            'breastCancerRiskPercentsColor': breastCancerRiskPercentsColor,
            'breastTableLines': breastTableLines,
        })
