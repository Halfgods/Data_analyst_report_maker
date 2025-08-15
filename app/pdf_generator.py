import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class DataAnalysisReportGenerator:
    """
    Comprehensive data analysis report generator for CSV datasets.
    Produces PDF-ready reports with visualizations and insights.
    """
    
    def __init__(self, csv_path: str):
        """
        Initialize the report generator with a CSV file path.
        
        Args:
            csv_path (str): Path to the CSV file to analyze
        """
        self.csv_path = csv_path
        self.df = None
        self.numeric_columns = []
        self.categorical_columns = []
        self.report_sections = {}
        
    def load_data(self) -> pd.DataFrame:
        """Load and prepare the dataset for analysis."""
        try:
            self.df = pd.read_csv(self.csv_path)
            self._identify_column_types()
            return self.df
        except Exception as e:
            raise Exception(f"Error loading CSV file: {e}")
    
    def _identify_column_types(self):
        """Identify numeric and categorical columns."""
        self.numeric_columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_columns = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    def generate_summary(self) -> str:
        """Generate dataset summary section."""
        total_rows, total_cols = self.df.shape
        missing_values = self.df.isnull().sum().sum()
        missing_percentage = (missing_values / (total_rows * total_cols)) * 100
        
        summary = f"""# Data Analysis Report

## 1. Summary

**Dataset Overview:**
- **Total Rows:** {total_rows:,}
- **Total Columns:** {total_cols}
- **Numeric Columns:** {len(self.numeric_columns)} ({', '.join(self.numeric_columns) if self.numeric_columns else 'None'})
- **Categorical Columns:** {len(self.categorical_columns)} ({', '.join(self.categorical_columns) if self.categorical_columns else 'None'})
- **Missing Values:** {missing_values:,} ({missing_percentage:.2f}%)

**Key Observations:**
- Dataset contains {total_rows} records with {total_cols} features
- {len(self.numeric_columns)} numeric and {len(self.categorical_columns)} categorical variables
- Missing data rate is {missing_percentage:.2f}% of total dataset
"""
        return summary
    
    def generate_descriptive_statistics(self) -> str:
        """Generate descriptive statistics section."""
        stats_section = "\n## 2. Descriptive Statistics\n\n"
        
        # Numeric columns statistics
        if self.numeric_columns:
            stats_section += "### Numeric Variables\n\n"
            numeric_stats = self.df[self.numeric_columns].describe()
            stats_section += "```python\n"
            stats_section += f"# Descriptive statistics for numeric columns\n{numeric_stats.to_string()}\n"
            stats_section += "```\n\n"
            
            # Additional statistics
            for col in self.numeric_columns:
                mode_val = self.df[col].mode().iloc[0] if not self.df[col].mode().empty else "N/A"
                stats_section += f"**{col}:**\n"
                stats_section += f"- Mean: {self.df[col].mean():.2f}\n"
                stats_section += f"- Median: {self.df[col].median():.2f}\n"
                stats_section += f"- Mode: {mode_val}\n"
                stats_section += f"- Std Dev: {self.df[col].std():.2f}\n"
                stats_section += f"- Range: {self.df[col].max() - self.df[col].min():.2f}\n\n"
        
        # Categorical columns statistics
        if self.categorical_columns:
            stats_section += "### Categorical Variables\n\n"
            for col in self.categorical_columns:
                value_counts = self.df[col].value_counts()
                stats_section += f"**{col}:**\n"
                stats_section += f"- Unique values: {self.df[col].nunique()}\n"
                stats_section += f"- Most frequent: {value_counts.index[0]} ({value_counts.iloc[0]} occurrences)\n"
                stats_section += f"- Distribution:\n"
                for val, count in value_counts.head(5).items():
                    percentage = (count / len(self.df)) * 100
                    stats_section += f"  - {val}: {count} ({percentage:.1f}%)\n"
                stats_section += "\n"
        
        return stats_section
    
    def generate_data_quality_insights(self) -> str:
        """Generate data quality insights section."""
        quality_section = "\n## 3. Data Quality Insights\n\n"
        
        # Missing values analysis
        missing_data = self.df.isnull().sum()
        missing_percentage = (missing_data / len(self.df)) * 100
        missing_df = pd.DataFrame({
            'Column': missing_data.index,
            'Missing_Count': missing_data.values,
            'Missing_Percentage': missing_percentage.values
        }).sort_values('Missing_Percentage', ascending=False)
        
        quality_section += "### Missing Values Analysis\n\n"
        quality_section += "```python\n"
        quality_section += f"# Missing values summary\n{missing_df.to_string(index=False)}\n"
        quality_section += "```\n\n"
        
        # Duplicates analysis
        duplicates = self.df.duplicated().sum()
        duplicate_percentage = (duplicates / len(self.df)) * 100
        
        quality_section += f"### Duplicates Analysis\n\n"
        quality_section += f"- **Total Duplicates:** {duplicates} ({duplicate_percentage:.2f}%)\n\n"
        
        # Data type consistency
        quality_section += "### Data Type Consistency\n\n"
        quality_section += "```python\n"
        quality_section += f"# Data types\n{self.df.dtypes.to_string()}\n"
        quality_section += "```\n\n"
        
        # Recommendations
        quality_section += "### Quality Recommendations\n\n"
        if missing_data.sum() > 0:
            quality_section += "- **Missing Values:** Consider imputation strategies based on data patterns\n"
        if duplicates > 0:
            quality_section += "- **Duplicates:** Review and remove duplicate records if appropriate\n"
        if len(self.numeric_columns) > 0:
            quality_section += "- **Outliers:** Check for outliers in numeric columns using boxplots\n"
        
        return quality_section
    
    def generate_visualizations(self) -> str:
        """Generate visualization section with Python code."""
        viz_section = "\n## 4. Visualizations\n\n"
        
        # Set style for better-looking plots
        viz_section += "```python\n"
        viz_section += "# Set up plotting style\n"
        viz_section += "plt.style.use('seaborn-v0_8')\n"
        viz_section += "sns.set_palette('husl')\n"
        viz_section += "fig, axes = plt.subplots(2, 2, figsize=(15, 12))\n"
        viz_section += "fig.suptitle('Data Analysis Visualizations', fontsize=16, fontweight='bold')\n\n"
        
        # 1. Numeric distributions (histograms)
        if self.numeric_columns:
            viz_section += "# 1. Numeric Variable Distributions\n"
            for i, col in enumerate(self.numeric_columns[:2]):  # Limit to 2 for 2x2 grid
                viz_section += f"axes[0, {i}].hist(df['{col}'], bins=20, alpha=0.7, edgecolor='black')\n"
                viz_section += f"axes[0, {i}].set_title(f'Distribution of {col}')\n"
                viz_section += f"axes[0, {i}].set_xlabel('{col}')\n"
                viz_section += f"axes[0, {i}].set_ylabel('Frequency')\n\n"
        
        # 2. Categorical frequency (bar charts)
        if self.categorical_columns:
            viz_section += "# 2. Categorical Variable Frequencies\n"
            for i, col in enumerate(self.categorical_columns[:2]):
                viz_section += f"value_counts = df['{col}'].value_counts()\n"
                viz_section += f"axes[1, {i}].bar(range(len(value_counts)), value_counts.values)\n"
                viz_section += f"axes[1, {i}].set_title(f'Frequency of {col}')\n"
                viz_section += f"axes[1, {i}].set_xlabel('{col}')\n"
                viz_section += f"axes[1, {i}].set_ylabel('Count')\n"
                viz_section += f"axes[1, {i}].set_xticks(range(len(value_counts)))\n"
                viz_section += f"axes[1, {i}].set_xticklabels(value_counts.index, rotation=45)\n\n"
        
        viz_section += "plt.tight_layout()\n"
        viz_section += "plt.show()\n"
        viz_section += "```\n\n"
        
        # 3. Boxplots for outliers
        if len(self.numeric_columns) >= 2:
            viz_section += "```python\n"
            viz_section += "# 3. Boxplots for Outlier Detection\n"
            viz_section += "fig, axes = plt.subplots(1, 2, figsize=(15, 6))\n"
            viz_section += f"df.boxplot(column=['{self.numeric_columns[0]}'], ax=axes[0])\n"
            viz_section += f"axes[0].set_title('Boxplot of {self.numeric_columns[0]}')\n"
            if len(self.numeric_columns) > 1:
                viz_section += f"df.boxplot(column=['{self.numeric_columns[1]}'], ax=axes[1])\n"
                viz_section += f"axes[1].set_title('Boxplot of {self.numeric_columns[1]}')\n"
            viz_section += "plt.tight_layout()\n"
            viz_section += "plt.show()\n"
            viz_section += "```\n\n"
        
        # 4. Correlation heatmap
        if len(self.numeric_columns) >= 2:
            viz_section += "```python\n"
            viz_section += "# 4. Correlation Heatmap\n"
            viz_section += "correlation_matrix = df[['" + "', '".join(self.numeric_columns) + "']].corr()\n"
            viz_section += "plt.figure(figsize=(10, 8))\n"
            viz_section += "sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,\n"
            viz_section += "            square=True, linewidths=0.5)\n"
            viz_section += "plt.title('Correlation Matrix of Numeric Variables')\n"
            viz_section += "plt.tight_layout()\n"
            viz_section += "plt.show()\n"
            viz_section += "```\n\n"
        
        # 5. Scatter plot for correlations
        if len(self.numeric_columns) >= 2:
            viz_section += "```python\n"
            viz_section += "# 5. Scatter Plot for Key Variables\n"
            viz_section += f"plt.figure(figsize=(10, 6))\n"
            viz_section += f"plt.scatter(df['{self.numeric_columns[0]}'], df['{self.numeric_columns[1]}'], alpha=0.6)\n"
            viz_section += f"plt.xlabel('{self.numeric_columns[0]}')\n"
            viz_section += f"plt.ylabel('{self.numeric_columns[1]}')\n"
            viz_section += f"plt.title(f'Relationship between {self.numeric_columns[0]} and {self.numeric_columns[1]}')\n"
            viz_section += f"plt.grid(True, alpha=0.3)\n"
            viz_section += f"plt.show()\n"
            viz_section += "```\n\n"
        
        return viz_section
    
    def generate_correlations_and_patterns(self) -> str:
        """Generate correlations and patterns section."""
        patterns_section = "\n## 5. Correlations & Patterns\n\n"
        
        if len(self.numeric_columns) >= 2:
            # Correlation analysis
            correlation_matrix = self.df[self.numeric_columns].corr()
            
            patterns_section += "### Correlation Analysis\n\n"
            patterns_section += "```python\n"
            patterns_section += f"# Correlation matrix\n{correlation_matrix.to_string()}\n"
            patterns_section += "```\n\n"
            
            # Find strongest correlations
            patterns_section += "### Strongest Correlations\n\n"
            correlations = []
            for i in range(len(self.numeric_columns)):
                for j in range(i+1, len(self.numeric_columns)):
                    corr_val = correlation_matrix.iloc[i, j]
                    correlations.append((self.numeric_columns[i], self.numeric_columns[j], corr_val))
            
            correlations.sort(key=lambda x: abs(x[2]), reverse=True)
            
            for var1, var2, corr in correlations[:3]:
                strength = "strong" if abs(corr) > 0.7 else "moderate" if abs(corr) > 0.3 else "weak"
                direction = "positive" if corr > 0 else "negative"
                patterns_section += f"- **{var1}** and **{var2}**: {corr:.3f} ({strength} {direction} correlation)\n"
            
            patterns_section += "\n"
        
        # Pattern analysis
        patterns_section += "### Key Patterns Identified\n\n"
        
        if self.numeric_columns:
            # Distribution patterns
            for col in self.numeric_columns:
                skewness = self.df[col].skew()
                if abs(skewness) > 1:
                    direction = "right-skewed" if skewness > 0 else "left-skewed"
                    patterns_section += f"- **{col}** shows {direction} distribution (skewness: {skewness:.2f})\n"
        
        if self.categorical_columns:
            # Categorical patterns
            for col in self.categorical_columns:
                value_counts = self.df[col].value_counts()
                if len(value_counts) <= 5:  # Only for columns with few categories
                    most_common = value_counts.index[0]
                    percentage = (value_counts.iloc[0] / len(self.df)) * 100
                    patterns_section += f"- **{col}** is dominated by '{most_common}' ({percentage:.1f}% of records)\n"
        
        return patterns_section
    
    def generate_insights_and_recommendations(self) -> str:
        """Generate actionable insights and recommendations."""
        insights_section = "\n## 6. Insights & Recommendations\n\n"
        
        insights = []
        
        # Insight 1: Data completeness
        missing_percentage = (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        if missing_percentage > 5:
            insights.append(f"**Data Quality Issue:** {missing_percentage:.1f}% missing data requires attention. Implement data validation and imputation strategies.")
        else:
            insights.append(f"**Data Quality:** Good data completeness with only {missing_percentage:.1f}% missing values.")
        
        # Insight 2: Numeric variable insights
        if self.numeric_columns:
            for col in self.numeric_columns:
                cv = self.df[col].std() / self.df[col].mean()  # Coefficient of variation
                if cv > 0.5:
                    insights.append(f"**High Variability:** {col} shows high variability (CV: {cv:.2f}), indicating diverse values that may need segmentation analysis.")
                break  # Limit to one insight per numeric column
        
        # Insight 3: Categorical distribution insights
        if self.categorical_columns:
            for col in self.categorical_columns:
                value_counts = self.df[col].value_counts()
                if len(value_counts) <= 5:
                    most_common_pct = (value_counts.iloc[0] / len(self.df)) * 100
                    if most_common_pct > 50:
                        insights.append(f"**Imbalanced Categories:** {col} is heavily skewed toward '{value_counts.index[0]}' ({most_common_pct:.1f}%). Consider balancing strategies for analysis.")
                break  # Limit to one insight per categorical column
        
        # Insight 4: Correlation insights
        if len(self.numeric_columns) >= 2:
            correlation_matrix = self.df[self.numeric_columns].corr()
            max_corr = correlation_matrix.values[correlation_matrix.values != 1].max()
            if max_corr > 0.7:
                insights.append(f"**Strong Correlation:** Found strong correlation ({max_corr:.2f}) between numeric variables. Consider multicollinearity in modeling.")
        
        # Insight 5: Sample size insight
        if len(self.df) < 100:
            insights.append(f"**Small Sample Size:** Dataset contains only {len(self.df)} records. Results may not be statistically significant for broader populations.")
        elif len(self.df) > 10000:
            insights.append(f"**Large Dataset:** {len(self.df):,} records provide robust statistical power for analysis and modeling.")
        
        # Add recommendations
        insights_section += "### Key Insights\n\n"
        for i, insight in enumerate(insights[:5], 1):
            insights_section += f"{i}. {insight}\n\n"
        
        insights_section += "### Actionable Recommendations\n\n"
        recommendations = [
            "**Data Collection:** Implement automated data validation to reduce missing values in future data collection.",
            "**Analysis Strategy:** Use stratified sampling if categorical variables are imbalanced for more representative analysis.",
            "**Modeling Approach:** Consider feature engineering and variable selection based on correlation analysis.",
            "**Monitoring:** Set up regular data quality checks and automated reporting for ongoing data health.",
            "**Documentation:** Maintain clear documentation of data sources, transformations, and business rules."
        ]
        
        for i, rec in enumerate(recommendations, 1):
            insights_section += f"{i}. {rec}\n\n"
        
        return insights_section
    
    def generate_complete_report(self) -> str:
        """Generate the complete data analysis report."""
        if self.df is None:
            self.load_data()
        
        report = ""
        report += self.generate_summary()
        report += self.generate_descriptive_statistics()
        report += self.generate_data_quality_insights()
        report += self.generate_visualizations()
        report += self.generate_correlations_and_patterns()
        report += self.generate_insights_and_recommendations()
        
        # Add footer
        report += "\n---\n"
        report += f"*Report generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        report += "*Data source: " + self.csv_path + "*\n"
        
        return report
    
    def save_report(self, output_path: str = None) -> str:
        """Save the report to a file."""
        if output_path is None:
            output_path = self.csv_path.replace('.csv', '_analysis_report.md')
        
        report = self.generate_complete_report()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return output_path


def generate_data_analysis_report(csv_path: str, output_path: str = None) -> str:
    """
    Convenience function to generate a complete data analysis report.
    
    Args:
        csv_path (str): Path to the CSV file to analyze
        output_path (str, optional): Path to save the report. If None, uses default naming.
    
    Returns:
        str: Path to the generated report file
    """
    generator = DataAnalysisReportGenerator(csv_path)
    return generator.save_report(output_path)


# Example usage and testing
if __name__ == "__main__":
    # Test with the provided test_data.csv
    try:
        report_path = generate_data_analysis_report("test_data.csv")
        print(f"Report generated successfully: {report_path}")
        
        # Also print a sample of the report
        with open(report_path, 'r') as f:
            report_content = f.read()
        print("\n" + "="*50)
        print("SAMPLE REPORT OUTPUT:")
        print("="*50)
        print(report_content[:1000] + "...\n[Report truncated for display]")
        
    except Exception as e:
        print(f"Error generating report: {e}")
