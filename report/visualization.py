import matplotlib.pyplot as plt
import seaborn as sns
from kpis import *

import warnings
warnings.filterwarnings("ignore")

sns.set(style="whitegrid")

# Hires by Technology
def plot_hires_by_technology():
    df = hires_by_technology()
    plt.figure(figsize=(10,6))
    sns.barplot(x='hires', y='technology', data=df, palette='viridis')
    plt.title('Hires by Technology')
    plt.xlabel('Number of Hires')
    plt.ylabel('Technology')
    plt.tight_layout()
    plt.show()

# Hires by Year
def plot_hires_by_year():
    df = hires_by_year()
    plt.figure(figsize=(8,5))
    sns.lineplot(x='year', y='hires', data=df, marker='o')
    plt.title('Hires by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Hires')
    plt.xticks(df['year'].astype(int)) 
    plt.tight_layout()
    plt.show()

# Hires by Seniority
def plot_hires_by_seniority():
    df = hires_by_seniority()
    plt.figure(figsize=(8,5))
    sns.barplot(x='hires', y='seniority', data=df, palette='coolwarm')
    plt.title('Hires by Seniority')
    plt.xlabel('Number of Hires')
    plt.ylabel('Seniority')
    plt.tight_layout()
    plt.show()

# Hires by Country and Year
def plot_hires_by_country_year():
    df = hires_by_country_year()
    plt.figure(figsize=(10,6))
    sns.lineplot(x='year', y='hires', hue='country', data=df, marker='o')
    plt.title('Hires by Country and Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Hires')
    plt.xticks(sorted(df['year'].unique()))
    plt.legend(title='Country')
    plt.tight_layout()
    plt.show()

# Hire Rate as Pie Chart
def plot_hire_rate():
    df = hire_rate()
    rate = df['hire_rate_percent'].values[0]
    labels = ['Hired', 'Not Hired']
    sizes = [rate, 100 - rate]
    colors = ['#66b3ff','#ff9999']
    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('Overall Hire Rate')
    plt.tight_layout()
    plt.show()

# Technology Candidate Ratio
def plot_tech_candidate_ratio():
    df = tech_candidate_ratio()
    plt.figure(figsize=(10,6))
    sns.barplot(x='hire_rate_percent', y='technology', data=df, palette='magma')
    plt.title('Hire Rate by Technology')
    plt.xlabel('Hire Rate (%)')
    plt.ylabel('Technology')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_hires_by_technology()
    plot_hires_by_year()
    plot_hires_by_seniority()
    plot_hires_by_country_year()
    plot_tech_candidate_ratio()
    plot_hire_rate()