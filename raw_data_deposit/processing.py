import os, json
import pandas as pd
import numpy as np

with open('outcomes.json', 'rb') as f:
    outcomes = json.load(f)

outcomes_check = {
    'Outcome': [k for k,v in outcomes.items() if v['type']=='Outcome'],
    'Outcome_Category': {k: v['choices'] for k,v in outcomes.items() if v['type']=='Outcome_Category'}}

outcomes_check_demo = {
    'Age': [y for y in range(1920,2009)],
    'Control': {k: v['choices'] for k,v in outcomes.items() if v['type']=='Control'}}

map_donation_fix = {str(v[:-1]): str(k) for k,v in outcomes['donation']['choices'].items()}
map_donation = {int(k): int(v[:-1]) for k,v in outcomes['donation']['choices'].items()}

def process_response(row):
    if row['outcome'] in outcomes_check['Outcome']: # outcome variable with value range [0,100]
        if (int(row['response']) >= 0) & (int(row['response']) <= 100):
            return 1 # valid response
        else:
            return 0 # invalid response
    else:
        if str(row['response']) in outcomes_check['Outcome_Category'][row['outcome']].keys():
            return 1 # valid response
        elif str(row['response'])+'$' in outcomes_check['Outcome_Category'][row['outcome']].values():
            return 2 # valid response; key-value swapped
        else:
            return 0 # invalid response

def fix_response(row):
    if (row['outcome'] == 'donation') & (row['validity']==2): # for 'donation', the LLM sometimes generated values -> map all to keys
        return map_donation_fix[row['response']]
    elif (row['outcome'] == 'donation') & (row['validity']==0): # for 'donation', the LLM sometimes generated values + \n -> map all to keys
        return map_donation_fix[row['response'].strip()]
    elif (row['condition'] == 'perfect prawn') & (row['response'] == 'No.'): # LLM generated verbatim label ("No.") instead of key -> return key
        return '2'
    else:
        return row['response']

def process_response_demo(row):
    if row['outcome'] in outcomes_check_demo['Control']:
        if str(row['response']) in outcomes_check_demo['Control'][row['outcome']].keys():
            return 1 # valid response
        elif str(row['response']) in outcomes_check_demo['Control'][row['outcome']].values():
            return 2 # valid response; key-value swapped
        else:
            return 0 # invalid response
    else:
        if (int(row['response']) >= 1920) & (int(row['response']) <= 2008):
            return 1 # valid response
        else: 
            return 0 # invalid response




####################################### Load data from per-condition prediction files
all_results = pd.DataFrame()
all_demographics = pd.DataFrame()

for condition in os.listdir('results'):
    if condition.startswith('.'):
        continue
        
    # check outcomes responses
    if not condition.endswith('_demo.csv'):
        
        df_results = pd.read_csv(f'results/{condition}', index_col=0, dtype=str)
        df_results.loc[:,'validity'] = df_results.apply(process_response, axis=1) # check validity
        df_results.loc[:,'response'] = df_results.apply(fix_response, axis=1) # fix invalid responses
        all_results = pd.concat([all_results, df_results])

    # check demographics responses
    else:
        df_results = pd.read_csv(f'results/{condition}', index_col=0, dtype=str)
        df_results.loc[:,'validity'] = df_results.apply(process_response_demo, axis=1)
        all_demographics = pd.concat([all_demographics, df_results])

# assemble outcomes responses into single rows=participants, columns=outcomes format
dict_conditions = {}

for i, row in all_results.iterrows():
    condition, persona = row['condition'], row['persona']
    if not condition in dict_conditions.keys():
        dict_conditions[condition] = {}
    if not persona in dict_conditions[condition].keys():
        dict_conditions[condition][persona] = {}
    dict_conditions[condition][row['persona']][row['outcome']] = row['response']

# conditions = [k for k in dict_conditions.keys()]
conditions = ['apple aardvark', 'crushing chicken; gross grasshopper; homely halibut', 'orchid orangutan; defiant dragonfly', 'complicated cockroach', 
'jealous jaguar', 'control baseball', 'control neckties', 'worse wildfowl', 'phony parrotfish', 'periwinkle partridge', 'flimsy fish',
'giant gibbon; brick bobcat', 'perfect prawn', 'limping llama; friendly frog', 'difficult dog', 'practical planarian', 'honored haddock',
'heartfelt hummingbird', 'control dances']
outcomes = [o for o in dict_conditions[conditions[0]]['p2571'].keys()]

all_responses = []
for i,c in enumerate(conditions):
    for p, p_responses in dict_conditions[c].items():
        persona_row = [f'c{str(i+1).zfill(2)}{p}', c]
        for o in outcomes:
            persona_row.append(p_responses[o])
        all_responses.append(persona_row)

df_responses = pd.DataFrame(all_responses, columns=['profile_id','condition']+outcomes)

### process outcomes to match codebook requirements; aggregate multi-item outcome measures

# enforce dtype to int
df_responses = df_responses.astype({c: int for c in list(df_responses.columns)[2:]})

# funding perceptions
df_responses.loc[:,'funding_perceptions'] = 100 - df_responses.loc[:,'funding_5']
df_responses = df_responses.drop(['funding_5'], axis=1)

# donations
df_responses.loc[:,'donation'] = df_responses.loc[:,'donation'].replace(map_donation)

# newsletter
df_responses.loc[:,'newsletter'] = df_responses.loc[:,'newsletter'].replace({2: 0, 1:1})

# map to correct column names (from codebook)
mat_codebook = pd.read_csv('codebook.csv')
dict_column_names = {row['qualtrics_label']:row['target_label'] for i, row in mat_codebook.iloc[6:50,:].iterrows()}
df_responses = df_responses.rename(columns=dict_column_names)

# prepare aggregation of multi-item outcome measures
outcomes_inst_trust = [v for v in dict_column_names.values() if v.startswith('inst_trust')]
outcomes_behavior = [v for v in dict_column_names.values() if v.startswith('behavior')]

# aggregate multi-item outcome measures
df_responses.loc[:,'trust_competence'] = [np.mean([row[f'trust_competence_{n}'] for n in range(1,4)]) for i, row in df_responses.iterrows()]
df_responses.loc[:,'trust_integrity'] = [np.mean([row[f'trust_integrity_{n}'] for n in range(1,4)]) for i, row in df_responses.iterrows()]
df_responses.loc[:,'trust_benevolence'] = [np.mean([row[f'trust_benevolence_{n}'] for n in range(1,4)]) for i, row in df_responses.iterrows()]
df_responses.loc[:,'trust_openness'] = [np.mean([row[f'trust_openness_{n}'] for n in range(1,4)]) for i, row in df_responses.iterrows()]
df_responses.loc[:,'trust_multidimensional'] = [np.mean([row['trust_competence'],row['trust_integrity'],row['trust_benevolence'],row['trust_openness']]) for i, row in df_responses.iterrows()]

df_responses.loc[:,'policy_role_mean'] = [np.mean([row[f'policy_role_{n}'] for n in range(1,5)]) for i, row in df_responses.iterrows()]
df_responses.loc[:,'inst_trust_mean'] = [np.mean([row[o] for o in outcomes_inst_trust]) for i, row in df_responses.iterrows()]
df_responses.loc[:,'concern_mean'] = [np.mean([row[f'concern_{n}'] for n in range(1,4)]) for i, row in df_responses.iterrows()]
df_responses.loc[:,'policy_specific_mean'] = [np.mean([row[f'policy_specific_{n}'] for n in range(1,8)]) for i, row in df_responses.iterrows()]
df_responses.loc[:,'behavior_mean'] = [np.mean([row[o] for o in outcomes_behavior]) for i, row in df_responses.iterrows()]

# subset to columns required for prediction file
df_responses = df_responses[['profile_id', 'trust_multidimensional', 'trust_competence_1', 'trust_competence_2', 'trust_competence_3', 
              'trust_integrity_1', 'trust_integrity_2', 'trust_integrity_3', 
              'trust_benevolence_1', 'trust_benevolence_2', 'trust_benevolence_3', 
              'trust_openness_1', 'trust_openness_2', 'trust_openness_3',
              'trust_post', 'distrust_post', 'funding_perceptions', 
              'policy_role_mean', 'inst_trust_mean', 'belief_post',
              'concern_mean', 'policy_general', 'policy_specific_mean',
              'behavior_mean', 'donation_ams', 'newsletter_signup']]

# assemble demographics responses into single rows=participants, columns=demographics format
demographics = list(set(all_demographics['outcome']))

dict_conditions_demo = {}

for i, row in all_demographics.iterrows():
    condition, persona = row['condition'], row['persona']
    if not condition in dict_conditions_demo.keys():
        dict_conditions_demo[condition] = {}
    if not persona in dict_conditions_demo[condition].keys():
        dict_conditions_demo[condition][persona] = {}
    dict_conditions_demo[condition][row['persona']][row['outcome']] = row['response']

all_responses_demo = []
for i,c in enumerate(conditions):
    for p, p_responses in dict_conditions_demo[c].items():
        persona_row = [f'c{str(i+1).zfill(2)}{p}', c]
        for d in demographics:
            persona_row.append(p_responses[d])
        all_responses_demo.append(persona_row)

df_controls = pd.DataFrame(all_responses_demo, columns=['profile_id','condition']+demographics)

### process demographics to match codebook requirements

# load mappings from demographics keys to values, ensuring that labels adhere to spelling etc. in codebook
with open('demo_mapping.json', 'rb') as f:
    mapping_demo = json.load(f)

for k,v in mapping_demo.items():
    d = k.split('_')[1]
    df_controls.loc[:,d] = df_controls.loc[:,d].replace(v)

# transform year_birth to age to age_band
def check_age(age):
    if age < 30:
        return '18-29'
    elif (age >= 30) & (age < 45):
        return '30-44'
    elif (age >= 45) & (age < 60):
        return '45-59'
    elif age >= 60:
        return '60+'
    else:
        return None

df_controls.loc[:,'age'] = [2026 - int(row['year_birth']) for i, row in df_controls.iterrows()]
df_controls.loc[:,'age_band'] = [check_age(row['age']) for i, row in df_controls.iterrows()]

# subset to required columns
df_controls = df_controls[['profile_id', 'condition', 'gender', 'age_band', 'race', 'education','income', 'party']]

# merge demographics and outcomes; prepare for submission
df_predictions = df_controls.merge(df_responses, on='profile_id', how='left')

# map condition codenames to condition names as required in codebook
df_codenames = pd.read_csv('condition_codenames.csv')
condition_map = {row['code_name']: row['title'] for i, row in df_codenames.iterrows()}

df_predictions.loc[:,'condition'] = df_predictions.loc[:,'condition'].replace(condition_map)
df_predictions = df_predictions.sort_values('profile_id')
df_predictions = df_predictions.reset_index(drop=True)

df_predictions.to_csv('team_4_T1_primary_v1.csv', index=False)