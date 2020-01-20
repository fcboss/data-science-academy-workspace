import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from category_encoders.target_encoder import TargetEncoder
from category_encoders.cat_boost import CatBoostEncoder

from sklearn.impute import SimpleImputer
k = 0.3434343434343435
class catboost_enc(BaseEstimator, TransformerMixin):
    def __init__(self,columns):
        self.columns = columns
    def fit(self,df,y=None):
        self.encoder = CatBoostEncoder(handle_unknown='value',cols=self.columns)#, use_cat_names=True)
        self.encoder = self.encoder.fit(df,y)
        return self
    def transform(self,df,y=None):
        df_ = df.copy()
        
        return self.encoder.transform(df_)
    
    

    
class target_enc(BaseEstimator, TransformerMixin):
    def __init__(self,columns):
        self.columns = columns
    def fit(self,df,y=None):
        self.encoder = TargetEncoder(handle_unknown='value',cols=self.columns)
        self.encoder = self.encoder.fit(df,y)
        return self
    def transform(self,df,y=None):
        df_ = df.copy()
        
        return self.encoder.transform(df_,y)
    
class inputer(BaseEstimator, TransformerMixin):
    def __init__(self,columns,strategy='constant',value = 0):
        self.columns = columns
        self.strategy = strategy
        self.value = value
    def fit(self,df,*kargs):
        self.encoder = SimpleImputer(strategy=self.strategy,fill_value=self.value)
        self.encoder = self.encoder.fit(df[self.columns])
        return self
    def transform(self,df,*kargs):
        df_ = df.copy()
        df_[self.columns] = self.encoder.transform(df_[self.columns])
        return df_






class column_select(BaseEstimator, TransformerMixin):
    def __init__(self,columns):
        self.columns = columns
    def fit(self,df,*kargs):
        return self
    def transform(self,df,*kargs):
        df_ = df.copy()
        return df_[self.columns]  
    

    
class coord_feats(BaseEstimator, TransformerMixin):
    def fit(self,df,*kargs):
        return self
    
    def transform(self,df,*kargs):
        df_ = df.copy()
        city_coords = pd.read_json('city_coords.json')
        df_[['city_long','city_lat']]= city_coords.loc[df_.InterventionLocationName].set_index(df_.index)     
        return df_



class strip_strings(BaseEstimator, TransformerMixin):
    def __init__(self,columns):
        self.columns = columns
    def fit(self,df,*kargs):
        return self
    def transform(self,df,*kargs):
        df_ = df.copy()
        for c in self.columns:
            df_[c]  = df_[c].str.strip().str.lower()
            print
        return df_
        
class control_discrimination(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.t_score_race_train = pd.read_csv('t_score_race_train.csv').set_index(['Department Name','Race_Ethnicity'])
        self.t_score_sex_train = pd.read_csv('t_score_sex_train.csv').set_index(['Department Name','SubjectSexCode'])
    def fit(self):

        return self
    def transform(self,df,y=None):
        df_ = df.copy()
        df_['Race_Ethnicity'] = df_.apply(self.four_races,axis=1)
        df_ = df_.apply(self.get_tscore,axis=1)
        df_['AdjustedContrabandIndicator'] = df_.apply(self.invert_if_discriminated,axis=1,args=['diff_means_race'])
        df_['AdjustedContrabandIndicator'] *= df_.apply(self.invert_if_discriminated,axis=1,args=['diff_means_sex'])
        
        return df_


    def get_tscore(self,df):
        t_score_race_train=self.t_score_race_train
        t_score_sex_train=self.t_score_sex_train
        try:       
            t_score_race = t_score_race_train.loc[df['Department Name'],df['Race_Ethnicity']].item()
        except:
            t_score_race = 0
        try:       
            t_score_sex = t_score_sex_train.loc[df['Department Name'],df['SubjectSexCode']].item()
        except:
            t_score_sex = 0
        df['diff_means_race']=t_score_race
        df['diff_means_sex']=t_score_sex

        return df
    def four_races(self,df):
        if(df.SubjectEthnicityCode=='H'):
            return 'H'
        elif(df.SubjectRaceCode=='W'):
            return 'W'
        elif(df.SubjectRaceCode=='B'):
            return('B')

        else:
            return 'O'
    def invert_if_discriminated(self,df,column_diff_means):
        diff = df[column_diff_means]
        if(df.ContrabandPredicted==0):
            return 0
        try:
            if(df.AdjustedContrabandIndicator==0):
                return 0
        except:
            pass
        
        result = (df['PredictedProbas']>k+(diff/0.7))*1
        if(result == 0):
            print("removed a ",df['Department Name'])
        return result

           