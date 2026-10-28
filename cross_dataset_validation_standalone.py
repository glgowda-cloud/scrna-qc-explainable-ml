import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, roc_auc_score, recall_score, precision_score
from xgboost import XGBClassifier

feats=['total_counts','pct_counts_ribo','pct_counts_hb','gene_complexity','log_total_counts','ribo_ratio','mt_ribo_ratio']
raw={k:pd.read_csv(f'features_{k}.csv',index_col=0) for k in 'ABC'}

rows=[]
for scaled in (False,True):
    data={}
    for k,df in raw.items():
        X=df[feats].reset_index(drop=True)
        if scaled: X=pd.DataFrame(StandardScaler().fit_transform(X),columns=feats)
        data[k]=(X,(df['cell_quality']=='Good').astype(int).reset_index(drop=True))
    for test in 'ABC':
        train=[k for k in 'ABC' if k!=test]
        Xtr=pd.concat([data[k][0] for k in train],ignore_index=True)
        ytr=pd.concat([data[k][1] for k in train],ignore_index=True)
        Xte,yte=data[test]
        m=XGBClassifier(n_estimators=300,max_depth=5,learning_rate=0.1,random_state=42,eval_metric='logloss').fit(Xtr,ytr)
        p=m.predict_proba(Xte)[:,1]; pred=(p>0.5).astype(int)
        rows.append({'Features':'standardised' if scaled else 'raw','Train on':'+'.join(train),'Test on':test,
                     'F1 (Good)':f1_score(yte,pred),'AUC':roc_auc_score(yte,p),
                     'Bad recall':recall_score(yte,pred,pos_label=0),'Bad precision':precision_score(yte,pred,pos_label=0)})
res=pd.DataFrame(rows).round(3)
print(res.to_string(index=False)); res.to_csv('cross_dataset_results.csv',index=False)