
This document provides SQL queries to analyze the **Rfam public SQL database** and extract specific insights.

## 1. How many types of tigers can be found in the taxonomy table of the dataset?

To count the number of unique tiger species in the `taxonomy` table, we use the following query:

```sql
SELECT COUNT(DISTINCT species) AS tiger_types
FROM taxonomy
WHERE species LIKE '%tigris%';
```

This query identifies all species containing `tigris` (scientific name for tigers) and counts the distinct types.

---

##  2. What is the "ncbi_id" of the Sumatran Tiger?

The **Sumatran Tiger**'s biological name is _Panthera tigris sondaica_. To find its `ncbi_id`, use:

```sql
SELECT ncbi_id
FROM taxonomy
WHERE species = 'Panthera tigris sondaica';
```

This returns the **NCBI taxonomy ID** of the Sumatran Tiger.

---

##  3. Find all the columns that can be used to connect the tables in the given database.

The Rfam database follows a relational model. The key columns linking tables are:

|Table|Column(s) Used for Joining|
|---|---|
|`rfamseq`|`rfamseq_acc` (links to `full_region`), `ncbi_id` (links to `taxonomy`)|
|`full_region`|`rfamseq_acc` (links to `rfamseq`), `rfam_acc` (links to `family`)|
|`family`|`rfam_acc` (links to `full_region`)|
|`taxonomy`|`ncbi_id` (links to `rfamseq`)|

These columns allow us to retrieve relevant biological information across tables.

---

## 4. Which type of rice has the longest DNA sequence?

To find the rice species (_Oryza_) with the longest DNA sequence, use:

```sql
SELECT tx.species, MAX(rs.length) AS max_length
FROM rfamseq rs
JOIN taxonomy tx ON rs.ncbi_id = tx.ncbi_id
WHERE tx.species LIKE '%Oryza%'
GROUP BY tx.species
ORDER BY max_length DESC
LIMIT 1;
```

This query:

- Joins `rfamseq` and `taxonomy` tables.
- Filters for **rice species** (`Oryza` genus).
- Retrieves the species with the **longest** DNA sequence.

---

## 5. Paginate a list of family names and their longest DNA sequence lengths (descending order)

We need to paginate families whose **DNA sequences exceed 1,000,000** base pairs. Fetching **page 9**, with **15 results per page**, the query is:

```sql
WITH FamilyMaxLengths AS (
    SELECT fr.rfam_acc, f.description, MAX(rs.length) AS max_length
    FROM full_region fr
    JOIN rfamseq rs ON fr.rfamseq_acc = rs.rfamseq_acc
    JOIN family f ON fr.rfam_acc = f.rfam_acc
    GROUP BY fr.rfam_acc, f.description
    HAVING MAX(rs.length) > 1000000
)
SELECT rfam_acc, description, max_length
FROM FamilyMaxLengths
ORDER BY max_length DESC
LIMIT 15 OFFSET 120;
```

### Explanation:

- **Step 1:** The **`WITH` clause** creates a temporary table with max sequence lengths.
- **Step 2:** The main query:
    - Filters families where `MAX(length) > 1,000,000`.
    - Orders by sequence length **descending**.
    - Uses `LIMIT 15 OFFSET 120` (pagination formula: `(page_number - 1) * results_per_page`).
