# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])

#rename columns from name to school
school_data.rename({'name':'school'},axis=1,inplace=True)
df_school_summary = school_data.copy()

#Generated df_school_district to only look at district schools
df_school_district = school_data[school_data['type'] == 'District']


#total number of schools in the District 
total_school_district = df_school_district.shape[0]


#Total number of student in the district
total_number_students_district = df_school_district['size'].sum()


#Total Budget of District
total_school_budget_district = df_school_district['budget'].sum()


#total average reading and math scores for the district
total_avg_reading_scores_district = school_data_complete.groupby(['type'])['reading_score'].mean()[0]
total_avg_math_scores_district = school_data_complete.groupby(['type'])['math_score'].mean()[0]


#Students must have a 70% on math or reading to pass 
pass_reading_district = school_data_complete[school_data_complete['reading_score'] >= 70]
pass_math_district = school_data_complete[school_data_complete['math_score'] >= 70]


#Count the number of students passing reading or math
passing_reading_count_district = pass_reading_district.groupby(['type'])['Student ID'].count()[0]
passing_math_count_district = pass_math_district.groupby(['type'])['Student ID'].count()[0]


#Calc for average students passing reading or math
avg_passing_math_district = (passing_math_count_district/total_number_students_district)*100
avg_passing_reading_district = (passing_reading_count_district/total_number_students_district)*100


#Calc for overall passing in the district
overall_passing_district = (avg_passing_math_district+avg_passing_reading_district)/2


#Generate dictionary for district summary dataframe
d = {'Total_School': [total_school_district],
     'Total_Students': [total_number_students_district],
     'Total_Budget': [total_school_budget_district],
     'Average_Math_score':[total_avg_math_scores_district],
     'Average_Reading_score':[total_avg_reading_scores_district],
     '%Passing Math': [avg_passing_math_district],
     '%Passing Reading': [avg_passing_reading_district],
     '%Overall Passing Rate': [overall_passing_district]}


#Generated dataframe using above dictionary
district_summary = pd.DataFrame(d)


#Arrange columns
district_summary = district_summary[['Total_School',
                                     'Total_Students',
                                     'Total_Budget',
                                     'Average_Math_score',
                                     'Average_Reading_score',
                                     '%Passing Math',
                                     '%Passing Reading',
                                     '%Overall Passing Rate' ]]


#Display dataframe for district summary
district_summary

#deleted column School ID
del df_school_summary['School ID']


#Calc the series for Per Student Budget
df_school_summary['Per Student Budget'] = df_school_summary['budget']/df_school_summary['size']


#Using groupy found the average reading and math scores for each school
avg_passing_math_reading_table = student_data.groupby(['school'])['reading_score','math_score'].mean().reset_index()


#merge average passing math and reading to school summary dataframe
df_school_summary = df_school_summary.merge(avg_passing_math_reading_table,on='school',how='outer')


#Students must have a 70% on math or reading to pass 
summary_criteria_passing_reading = student_data[student_data['reading_score'] >= 70]
summary_criteria_passing_math = student_data[student_data['math_score'] >= 70]


#Count the number of students passing reading and rename column
passing_reading_count_summary =summary_criteria_passing_reading.groupby(['school'])['reading_score'].count().reset_index()
passing_reading_count_summary.rename({'reading_score':'reading_count'},axis=1,inplace=True)


#Count the number of students passing math and rename column
passing_math_count_summary = summary_criteria_passing_math.groupby(['school'])['math_score'].count().reset_index()
passing_math_count_summary.rename({'math_score':'math_count'},axis=1,inplace=True)


#merge over count to passing math dataframe
passing_count = passing_math_count_summary.merge(passing_reading_count_summary,on='school',how='inner')


#merge overall passing count to school summary dataframe
df_school_summary = df_school_summary.merge(passing_count,on='school',how='outer')


#Calc for % Passing math and reading 
df_school_summary['% Passing Math'] = (df_school_summary['math_count']/df_school_summary['size'])*100
df_school_summary['% Passing Reading'] = (df_school_summary['reading_count']/df_school_summary['size'])*100


#delete math and reading count from dataframe
del df_school_summary['math_count']
del df_school_summary['reading_count']


#Calc for % Overall Passing series in school summary dataframe
df_school_summary['% Overall Passing'] = (df_school_summary['% Passing Math'] + df_school_summary['% Passing Reading'])/2


#rename axis for reading and math scores to average reading and average math scores in school summary dataframe 
df_school_summary.rename({'reading_score':'Average Reading Score',
                            'math_score': 'Average Math Score'},axis= 1 , inplace= True)

#display school summary dataframe
df_school_summary.(subset=['Average Reading Score',
                            'Average Math Score',
                            '% Passing Math',
                            '% Passing Reading',
                            '% Overall Passing'])

#deleted column School ID
del df_school_summary['School ID']


#Calc the series for Per Student Budget
df_school_summary['Per Student Budget'] = df_school_summary['budget']/df_school_summary['size']


#Using groupy found the average reading and math scores for each school
avg_passing_math_reading_table = student_data.groupby(['school'])['reading_score','math_score'].mean().reset_index()


#merge average passing math and reading to school summary dataframe
df_school_summary = df_school_summary.merge(avg_passing_math_reading_table,on='school',how='outer')


#Students must have a 70% on math or reading to pass 
summary_criteria_passing_reading = student_data[student_data['reading_score'] >= 70]
summary_criteria_passing_math = student_data[student_data['math_score'] >= 70]


#Count the number of students passing reading and rename column
passing_reading_count_summary =summary_criteria_passing_reading.groupby(['school'])['reading_score'].count().reset_index()
passing_reading_count_summary.rename_axis({'reading_score':'reading_count'},axis=1,inplace=True)


#Count the number of students passing math and rename column
passing_math_count_summary = summary_criteria_passing_math.groupby(['school'])['math_score'].count().reset_index()
passing_math_count_summary.rename_axis({'math_score':'math_count'},axis=1,inplace=True)


#merge over count to passing math dataframe
passing_count = passing_math_count_summary.merge(passing_reading_count_summary,on='school',how='inner')


#merge overall passing count to school summary dataframe
df_school_summary = df_school_summary.merge(passing_count,on='school',how='outer')


#Calc for % Passing math and reading 
df_school_summary['% Passing Math'] = (df_school_summary['math_count']/df_school_summary['size'])*100
df_school_summary['% Passing Reading'] = (df_school_summary['reading_count']/df_school_summary['size'])*100


#delete math and reading count from dataframe
del df_school_summary['math_count']
del df_school_summary['reading_count']


#Calc for % Overall Passing series in school summary dataframe
df_school_summary['% Overall Passing'] = (df_school_summary['% Passing Math'] + df_school_summary['% Passing Reading'])/2


#rename axis for reading and math scores to average reading and average math scores in school summary dataframe 
df_school_summary.rename({'reading_score':'Average Reading Score',
                            'math_score': 'Average Math Score'},axis= 1 , inplace= True)

#display school summary dataframe
df_school_summary(subset=['Average Reading Score',
                            'Average Math Score',
                            '% Passing Math',
                            '% Passing Reading',
                            '% Overall Passing'])

#Using the school summary dataframe found the Bottom Perfroming School by % Overall Passing column
df_Bottom_Performing_Schools_By_Passsing_Rate = df_school_summary.sort_values(by=['% Overall Passing']).head(5)

#Display Bottom Performing Schools (By Passing Rate) 
df_Bottom_Performing_Schools_By_Passsing_Rate(subset=['% Overall Passing'])

#Using a pivot table grouped the math scores by average grade
df_math_scores__grade =pd.pivot_table(df_students,values=['math_score'],index=['school'],columns=['grade'])
df_math_scores__grade = df_math_scores__grade.reindex_axis(labels=['9th',
                                                                   '10th',
                                                                   '11th',
                                                                   '12th'],axis=1,level=1)
#Display Math Scores by Grade
df_math_scores__grade

#Using a pivot table grouped the reading scores by average grade
df_reading_scores__grade=pd.pivot_table(df_students,values=['reading_score'],index=['school'],columns=['grade'])


#reindex axis for reading scores by grade dataframe
df_reading_scores__grade = df_reading_scores__grade.reindex_axis(labels=['9th',
                                                                         '10th',
                                                                         '11th',
                                                                         '12th'],axis=1,level=1)
#Display Reading Scores by Grade
df_reading_scores__grade

# Sample bins. Feel free to create your own bins.
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]

#Copy school summary dataframe to new dataframe titled scores by school spending
scores_by_school_spending = df_school_summary.copy()

#assigned labels for bins
label_spending = np.array(["<$585", "$585-615", "$615-645", "$645-675"])

#bin Per Student Budget column
scores_by_school_spending['Per Student Budget'] = pd.qcut(scores_by_school_spending['Per Student Budget'],4,labels=label_spending,precision=0)

#Display scores by school spending 
scores_by_school_spending.groupby(['Per Student Budget'])['Average Reading Score', 
                                                          'Average Math Score',
                                                          '% Passing Math',
                                                          '% Passing Reading',
                                                          '% Overall Passing'].mean()
# Sample bins. Feel free to create your own bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

#Copy school summary dataframe to new dataframe titled scores by school size
scores_by_school_size = df_school_summary.copy()


#label small, medium, and large for bins
label = np.array(['small','medium','large'])


#bin school size 
scores_by_school_size['size'] = pd.qcut(scores_by_school_size['size'],3,labels=label)

#Use groupby to find the average scores for reading, math, % Passing Math, % Passing Reading, and % Overall Passing 
scores_by_school_size = scores_by_school_size.groupby(['size'])['Average Reading Score',
                                                                'Average Math Score', 
                                                                '% Passing Math',
                                                                '% Passing Reading',
                                                                '% Overall Passing'].mean().reset_index()

#reindex axis for dataframe 
scores_by_school_size = scores_by_school_size.reindex_axis(labels=[2,1,0])
scores_by_school_size.set_index(keys=['size'],inplace=True)

#Display scores by school size dataframe
scores_by_school_size

#Copy school summary dataframe to new dataframe titled scores by school type
scores_by_school_type = df_school_summary.copy()


#Use groupby to find the average scores for reading, math, % Passing Math, % Passing Reading, and % Overall Passing 
scores_by_school_type = scores_by_school_type.groupby(['type'])['Average Reading Score',
                                                                'Average Math Score',
                                                                '% Passing Math',
                                                                '% Passing Reading',
                                                                '% Overall Passing'].mean().reset_index()
#Set index to type
scores_by_school_type.set_index('type',inplace=True)

#Display scores by school type dataframe
scores_by_school_type
