# TITLE
Reference-dependent instability in spatial agricultural suitability assessment: Evidence from rice cultivation-system transfer in Europe

# ABSTRACT
Climatic thresholds transferred from a reference region are widely used to screen where a cropping system could be introduced, yet the reliability of the resulting maps is rarely assessed against mapped existing cultivation. I assess a growing-degree-day (GDD10) gate for transferring the cold-region rice system of Hokkaido, Japan, to {inc_Mha} Mha of incumbent arable land in Europe (excluding Russia), using WorldClim 2.1 climate normals, MapSPAM 2010 crop harvested areas and the Global Map of Irrigation Areas on one 5′ grid. Calibrated on Hokkaido rice area, the reference is {T_star} GDD10; {pct_T}% of incumbent arable land passes it, but only {pct_aei}% also has mapped irrigation infrastructure. In a controlled contrast for Germany, the pass share falls from {de_T}% to {de_900}% when a point-derived reference (~900 GDD10) replaces the grid-calibrated one, whereas recalibrating at 2.5′–10′ changes it by at most {de_res_pp} percentage points. A threshold sweep (0–1800 GDD10) shows that the {rice_kha} thousand ha of mapped European rice harvested area is a weak arbiter between these references: raising the threshold from {T_star} to 900 removes {crop_drop_pp} percentage points of candidate area but increases omitted rice area only from {om_T}% to {om_900}%. Omissions are concentrated in low-density allocation cells at the climatic margins of Italy, France and Ukraine and roughly double under one-cell grid shifts. Presence-only coverage therefore constrains only implausibly strict thresholds; reference construction, not grid support, is the dominant and unvalidated source of uncertainty in transferred-threshold suitability maps.

# KEYWORDS
growing degree days; threshold sensitivity; omission analysis; MapSPAM; irrigation infrastructure; classification stability

# 1. Introduction
Spatial suitability assessment is a routine instrument of environmental and agricultural planning. Typical studies combine climatic, edaphic and topographic layers by weighted overlay, fuzzy membership or species-distribution modelling to delimit zones in which a crop could be grown (Azadi et al., 2023; Bazkiaee et al., 2024; Mohamed et al., 2019; Van et al., 2022). The same logic is applied at continental and global extents, where gridded climate normals and crop maps are screened against crop-specific requirements (Ojara et al., 2021; Zabel et al., 2014) and used to discuss crop migration under warming (King et al., 2018; Sloat et al., 2020). Several assessments have shown that results depend on the decision rule, the weighting scheme and the spatial support of the inputs (Bagwan & Gavali, 2024; Jelinski & Wu, 1996; Malone et al., 2015; Rashidi & Sharifian, 2022; Tenerelli & Carver, 2012; Xu & Zhang, 2013). Suitability is therefore not an intrinsic property of a land parcel but a product of the assessment specification (Snelder et al., 2023).

A specific and common specification problem arises when a threshold is transferred from a reference region where a system is already practised to a region where it is not. The threshold is then an empirical reference, and its value depends on how the reference is constructed: which climate source, period and temporal aggregation are used, whether the reference is a station point or an area-weighted distribution over mapped cultivation, and which quantile of that distribution is taken. These choices are rarely reported as uncertainty, and the transferred map is rarely confronted with where the crop is actually mapped in the target region. Where it is, the comparison is usually reported as a single agreement figure at the chosen threshold, which cannot reveal whether the reference data could distinguish that threshold from plausible alternatives.

This study assesses that reliability problem for one concrete case: screening European arable land for the cold-region rice cultivation system of Hokkaido, Japan, the northernmost large-scale paddy rice system. I do not propose a new suitability method or a physiological threshold. Instead, I ask four assessment questions that can be answered with existing public monitoring and census-derived data. (i) How much does the construction of the empirical reference change the classification of a target region? (ii) How much of the mapped existing rice harvested area in Europe is omitted by the thermal gate across a full range of thresholds? (iii) What is the trade-off between the area retained for next-stage assessment and the omitted existing rice area, and does that trade-off discriminate between competing references? (iv) How do the geographic denominator, the grid support and a non-compensatory irrigation-infrastructure gate change the interpretation? The contribution is empirical evidence on the instability and the limited verifiability of a transferred-threshold assessment, together with an explicit statement of what the available reference data can and cannot validate.

# 2. Data and methods
## 2.1 Domain, spatial unit and denominator
The assessment domain is Europe as delineated by Natural Earth 1:50 m country boundaries (Natural Earth, 2024), excluding Russia, whose territory is truncated by the 45°E edge of the 11°W–45°E, 34°N–71.5°N processing window. Transcontinental countries are assigned by the Natural Earth continent attribute, so that, for example, Türkiye, Georgia and Azerbaijan fall outside the European domain. All layers share one regular 5′ latitude–longitude grid aligned to the global origin (−180°, 90°). The denominator is the 2010 harvested area of wheat, maize, barley and potato in MapSPAM 2010 v2.0, all technologies combined (IFPRI, 2019; Yu et al., 2020), termed incumbent arable land. It totals {inc_Mha} Mha in the domain and measures where arable cropping already occurs and where a new system would compete with incumbent crops; it is not an estimate of convertible land. Areas are harvested hectares as provided by MapSPAM; no additional pixel-area weighting is applied to them. Cell areas computed on the WGS84 authalic sphere are used only to express irrigation-equipped area as a share of each cell. The data sources and their roles are listed in Table 1.

[[TABLE:data]]

## 2.2 Thermal gate and reference construction
Commercial rice production in Hokkaido relies on ultra-early japonica cultivars, heated nurseries, transplanting and warm-water irrigation (MAFF, 2024). Hokkaido is used as the reference for this transferable cold-region system, not as a universal physiological limit. Thermal accumulation is GDD10, the sum of daily mean temperature above 10 °C over the season window of the original analysis pipeline, which runs from about 29 April to 11 September. On the grid, GDD10 is computed from WorldClim 2.1 monthly mean temperature for 1970–2000 (Fick & Hijmans, 2017), weighting each month by the number of its days inside the window. The primary grid reference T* is calibrated on the same surface as the 5th percentile of GDD10 over Hokkaido rice cells, weighted by MapSPAM 2010 rice harvested area ({hok_rice_kha} thousand ha). The estimand of T* is therefore the GDD10 exceeded by 95% of mapped Hokkaido rice harvested area on this specific climate surface, which is {T_star} GDD10; the 1st, 10th and 50th percentiles are {P01}, {P10} and {P50} GDD10.

The alternative reference used in an earlier version of the pipeline was a NASA POWER point series for 2000–2024 at 43.2°N, 143.0°E (NASA POWER Project, 2025; evaluated by Bai et al., 2010), which yields about 900 GDD10. To separate the effect of reference construction from that of spatial support, I recomputed the threshold along a controlled path on a fixed WorldClim 5′ target surface: point daily data 2000–2024, the same point for 1981–2000, a monthly-mean formula, the co-located WorldClim cell, the Hokkaido rice-area median and finally the rice-area 5th percentile. Grid support was assessed separately by recalibrating the 5th-percentile reference on 2.5′, 5′ and 10′ surfaces and applying each to its own surface. The same decomposition was repeated for a calendar June–September window.

## 2.3 Irrigation-infrastructure gate
A cell passes the infrastructure gate if its area equipped for irrigation in the Global Map of Irrigation Areas v5 (Siebert et al., 2013) is at least 10% of the cell area. This layer records equipped infrastructure around 2005 compiled from subnational statistics. It is not evidence of water allocation, rice-specific field infrastructure such as levelled basins and drainage, or implementation feasibility. The thermal and infrastructure gates are combined non-compensatorily: a cell is a candidate for next-stage assessment only if it passes both. I use "candidate" strictly in this sense; candidate area is not feasible or recommended land.

## 2.4 Threshold sweep against mapped existing rice area
The primary sweep holds the climate surface, season window, domain, denominator and weights fixed and varies only the threshold from 0 to 1800 GDD10 in steps of 25, adding the named references in Table 2. For each threshold *T* I compute the candidate share of incumbent arable land, weighted by incumbent harvested area *a*ᵢ, and the omitted share of mapped rice harvested area, weighted by rice harvested area *r*ᵢ, where *G*ᵢ is the GDD10 of cell *i*:

[[EQ:candidate]]

[[EQ:omission]]

Here 1[·] is the indicator function and the sums run over domain cells with incumbent arable land (for *C*) or mapped rice area (for *O*).

Rice harvested area is taken from the same MapSPAM 2010 release (all technologies), covering {rice_kha} thousand ha in {rice_cells} domain cells. Omission is computed over all rice cells; the variant restricted to cells that also contain incumbent arable land, used in earlier reports, is shown for comparison. Because the threshold is calibrated in Hokkaido and evaluated on European rice cells, the check is out of sample with respect to the calibration region. It is, however, a presence-only coverage check. Non-rice cropland is not an independently verified negative, because rice is excluded from most of Europe by water, soils, markets and institutions rather than by temperature alone. I therefore do not compute specificity, precision, F1 scores or receiver-operating-characteristic statistics, and the omission–candidate curve is not an ROC curve. On a fixed surface, *C*(*T*) cannot increase and *O*(*T*) cannot decrease with *T*; this monotonicity is mechanical. The information of the sweep lies in where along the threshold axis omissions begin to rise, relative to the competing references, and in how strongly candidate area changes over thresholds that the rice data cannot distinguish.

[[TABLE:refs]]

## 2.5 Omission geography, grid alignment and reference-data independence
Omitted rice area is mapped and summarised by country, by 8-connected cluster on the 5′ grid and by rice density within the cell. To test sensitivity to co-registration between MapSPAM and WorldClim, the rice layer was shifted by one cell in each of the eight directions, omission was recomputed with a 3 × 3 neighbourhood rule (a cell counts as omitted only if all neighbouring cells fail), with 2.5′ sub-cell pass fractions and on the native 10′ surface. Leave-one-country-out recomputation provides a range of omission shares that is a scenario range, not a statistical confidence interval; I do not bootstrap individual cells, because adjacent cells share climate and allocation information and are not independent observations.

MapSPAM harvested area is not an independent field observation. MapSPAM allocates national and subnational production statistics to grid cells using cropland extent, irrigation maps and crop-suitability information (Yu et al., 2020). Its rice layer is therefore partly conditioned on irrigation and climate information related to the gates evaluated here. The infrastructure gate shares the irrigation-statistics lineage of the MapSPAM irrigated technology, so agreement between mapped rice and the infrastructure gate is not treated as validation. For the thermal gate, the Hokkaido reference was calibrated on MapSPAM rice area in Japan, while the European rice area serves as the evaluation set; both originate from the same modelled product, so the check is out of region but not out of product.

## 2.6 Classification stability
Agreement between the primary specification and alternatives was computed on incumbent arable land: the point-derived 900 GDD10 reference, a June–September window recalibrated to its own 5th percentile ({T_cal} GDD10), 2.5′ and 10′ surfaces recalibrated to their own 5th percentiles ({t25} and {t10} GDD10), and the Hokkaido rice-area median. For each pair I report the area-weighted agreement share and the Jaccard index of the pass sets, and I map the cells whose class changes. Stability between specifications is reported separately from coverage of mapped rice area; neither establishes the agronomic validity of a gate.

## 2.7 Software and use of AI-assisted tools
All calculations were performed in Python with rasterio, geopandas, NumPy, SciPy and pandas. Every number in the text, tables and figures is generated by scripts from the cited data. An AI-assisted coding and writing agent (Devin, Cognition AI) was used to write and audit analysis scripts, reproduce calculations and draft text; I reviewed and edited all content and take full responsibility for it.

# 3. Results
## 3.1 Reference construction dominates the Germany contrast
In Germany ({de_inc_Mha} Mha of incumbent arable land) the pass share is {de_T}% at T* but {de_900}% at the point-derived reference (Fig. 1). Along the controlled path on a fixed 5′ surface, changing the period from 2000–2024 to 1981–2000, replacing daily with monthly aggregation and moving from the point to its WorldClim cell raises the pass share to {de_cell}%; replacing the single cell with the Hokkaido rice-area distribution gives {de_P50}% at the median and {de_T}% at the 5th percentile. In contrast, recalibrating the 5th-percentile reference at 2.5′, 5′ and 10′ yields thresholds of {t25}, {T_star} and {t10} GDD10 and changes the German pass share by at most {de_res_pp} percentage points. The quantile and the point-versus-distribution construction of the reference, not grid resolution, account for most of the contrast.

[[FIG:germany]]

## 3.2 Thermal and infrastructure gates across Europe
At T*, {pct_T}% of European incumbent arable land ({pass_Mha} Mha) passes the thermal gate, {pct_900}% at 900 GDD10 and {pct_1076}% at {eu_P05} GDD10, the 5th percentile of mapped European rice area (Table 2). Adding the infrastructure gate reduces the candidate share at T* to {pct_aei}% ({aei_Mha} Mha), and to {pct_aei_900}% at 900 GDD10. For most of the thermal range the infrastructure gate rather than the thermal gate determines the size of the candidate area, and no thermal surplus compensates for missing infrastructure.

## 3.3 Threshold-dependent omission of mapped rice area
Mapped European rice harvested area lies predominantly in warm cells: its rice-area-weighted GDD10 median is {eu_P50} and its 5th percentile is {eu_P05}. Consequently the omission curve is nearly flat over the range of competing Hokkaido references (Fig. 2). Omission is {om_P01}% at the Hokkaido 1st percentile ({P01} GDD10), {om_T}% at T*, {om_P50}% at the Hokkaido median and {om_900}% at 900 GDD10; it reaches {om_1100}% at 1100, {om_1300}% at 1300 and {om_1400}% at 1400 GDD10. Restricted to rice cells that also contain incumbent arable land, omission at T* is {om_T_inc}%, the figure reported in earlier versions; the difference arises from {rice_noinc_kha} thousand ha of mapped rice in cells without incumbent crops.

[[FIG:curve]]

## 3.4 Candidate area versus omitted rice area
The trade-off curve shows that the references proposed for Hokkaido differ greatly in candidate area but hardly in omission (Fig. 3). Moving from T* to 900 GDD10 removes {crop_drop_pp} percentage points ({crop_drop_Mha} Mha) of incumbent arable land from the thermal pass set but adds only {om_rise_pp} percentage points of omitted rice area. In Germany the same move removes {de_drop_pp} percentage points, while MapSPAM maps no rice in Germany. Omission first exceeds 10% of mapped rice area at {T_om10} GDD10. The mapped rice data therefore reject thresholds that would exclude much of current Mediterranean and Danubian rice production but cannot discriminate among the Hokkaido-derived references that drive the European and German results.

[[FIG:tradeoff]]

## 3.5 Geography and robustness of omissions
At T*, the {om_T_ha} ha of omitted rice area fall in {om_cells} cells forming {om_clusters} clusters; the five largest clusters contain {om_top5}% of the omitted area, and {om_ital_fr}% of it lies in Italy and France (Fig. 4). In {om_fringe_cells_pct}% of omitted cells, holding {om_fringe_pct}% of omitted area, rice occupies less than 1% of the cell, which is characteristic of statistical allocation to the cool upland margins of rice-producing administrative units, for example in northern Italy, south-eastern France and North Macedonia, rather than of established paddy districts. The omission share is sensitive to co-registration: one-cell shifts of the rice layer give {sh_min}–{sh_max}% at T*, and a 3 × 3 neighbourhood rule reduces it to {nb3_T}% (Table 3). Leave-one-country-out recomputation gives {loco_T} at T* and {loco_900} at 900 GDD10. These ranges are comparable in magnitude to the difference between T* and 900 GDD10, reinforcing that the omission check cannot rank these references.

[[FIG:geo]]

[[TABLE:align]]

## 3.6 Classification stability between specifications
Agreement with the primary specification is high for alternatives that keep the reference construction and vary support or window, and low for alternatives that change the reference itself (Table 4). The Jaccard index of the thermal pass sets is {jac_25} for the recalibrated 2.5′ surface, {jac_10} for the recalibrated 10′ surface and {jac_cal} for the recalibrated June–September window, but {jac_900} for the 900 GDD10 reference and {jac_P50} for the Hokkaido median. In Germany the Jaccard index against the 900 GDD10 reference is {jac_de_900}. The disagreement between T* and 900 GDD10 covers {dis_Mha} Mha and forms a contiguous belt from western France through the Benelux countries, Germany, Poland and Belarus to the Baltic states (Fig. 5), which is the region in which transfer proposals for cold-tolerant rice would be most consequential. Of the candidate area that passes both gates at T*, {tm_lost_Mha} Mha fails the thermal gate at 900 GDD10.

[[FIG:disagree]]

[[TABLE:stab]]

# 4. Discussion
## 4.1 Instability versus validity
Three results need to be kept apart. First, the classification of the target region is unstable with respect to reference construction: Germany changes from almost fully passing to almost fully failing depending on whether the reference is an area-weighted lower quantile on the target-consistent grid or a station-like point value. Second, the classification is stable with respect to grid support once the reference is recalibrated on each surface: scale effects of the modifiable areal unit problem (Jelinski & Wu, 1996) are present but small in this case, whereas the spatially explicit sensitivity to the reference itself (cf. Xu & Zhang, 2013) is large. Third, the available reference data on existing rice area validate neither specification in the critical range. Low omission at T* demonstrates that the gate does not exclude current European rice production, but because European rice is mapped mainly in cells far warmer than any Hokkaido reference, omission would remain at or below 5% for every threshold up to {T_om5} GDD10, which by construction is the 5th percentile of mapped European rice area. A permissive threshold can produce low omission mechanically, and the omission curve is informative only where it rises.

## 4.2 Implications for environmental suitability assessment
For transferred-threshold assessments, this case suggests four reporting practices. The estimand of the reference should be stated, including source, period, aggregation, spatial support and quantile, because these choices change results by an order of magnitude more than resolution does. The threshold should be swept, and the candidate area reported together with the omission of mapped existing cultivation, so that readers see which part of the threshold range the reference data can constrain. The independence of the reference data should be audited: crop maps produced by statistical allocation share inputs with the gates and are not field observations of presence or absence. Finally, non-compensatory gates such as irrigation infrastructure should be reported separately from climatic gates, because they can determine the candidate area regardless of the climatic reference. These practices complement multi-criteria uncertainty analysis (Malone et al., 2015; Tenerelli & Carver, 2012) and the recognition that suitability depends on the assessment frame (Snelder et al., 2023). They are relevant to suitability studies that rely on a few reference sites or on field-survey presence points (Benti et al., 2022; Wang et al., 2024).

## 4.3 Limitations and external validation
The analysis uses 1970–2000 climate normals and 2010 crop maps; it does not assess recent warming or observed land-use change. MapSPAM rice area is a modelled allocation of statistics, not mapped paddy fields, and harvested area may differ from physical area. GMIA records equipped infrastructure around 2005, not current water rights or rice-ready fields. The thermal gate represents one cold-region system; other cultivars, sowing dates or water-warming practices would require their own references. No independent negative data exist for rice absence, so commission cannot be estimated. An external validation would require field- or parcel-level observations of rice trials or cultivation near the climatic margin, for example national parcel registers or experimental plantings in central Europe, together with records of failed or abandoned attempts.

# 5. Conclusions
Transferring a thermal threshold from Hokkaido to Europe yields a candidate area that depends mainly on how the reference is constructed. Mapped existing rice area confirms that the gate does not exclude current European production, but it cannot discriminate between references that differ by tens of millions of hectares of candidate land, and irrigation infrastructure further reduces the candidate area to {pct_aei}% of incumbent arable land. Suitability maps based on transferred thresholds should therefore report reference construction, threshold sweeps and the limited verifiability of presence-only reference data as part of the assessment.

# DECLARATIONS
## Funding
This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.
## Competing interests
The author has no relevant financial or non-financial interests to disclose.
## Ethics approval and consent
Not applicable; the study uses only publicly available gridded environmental and agricultural data.
## Data availability
All input datasets are publicly available from the sources cited in Table 1 and the References. Derived outputs, including the threshold sweep, omission tables and classification-stability tables, are available in the public repository {repo_url}. GMIA is not redistributed because of its licence; the repository contains an acquisition ledger with source URLs, retrieval times, file sizes and SHA-256 checksums.
## Code availability
All analysis and figure scripts are available in the public repository {repo_url}.
## Author contributions
Tatsuki Onishi: conceptualization, methodology, software, formal analysis, data curation, visualization, writing – original draft, writing – review and editing.

# REFERENCES
Azadi, A., Jalali, A. S., & Navidi, M. N. (2023). Land evaluation approaches comparing TOPSIS and SAW with parametric methods for rice cultivation. *Environmental Monitoring and Assessment, 195*(11), 1296. https://doi.org/10.1007/s10661-023-11849-8

Bagwan, W. A., & Gavali, R. S. (2024). Does spatial resolution matter in the estimation of average annual soil loss by using RUSLE?—a study of the Urmodi River Watershed (Maharashtra), India. *Environmental Monitoring and Assessment, 196*(2), 167. https://doi.org/10.1007/s10661-024-12341-7

Bai, J., Chen, X., Dobermann, A., Yang, H., Cassman, K. G., & Zhang, F. (2010). Evaluation of NASA satellite- and model-derived weather data for simulation of maize yield potential in China. *Agronomy Journal, 102*(1), 9–16. https://doi.org/10.2134/agronj2009.0085

Bazkiaee, P. A., Kamkar, B., Amiri, E., Kazemi, H., Rezaei, M., & Araji, H. A. (2024). Multi-criteria GIS-based land suitability analysis for rice cultivation: A case study in Guilan Province, Iran. *Environmental Monitoring and Assessment, 196*(7), 680. https://doi.org/10.1007/s10661-024-12811-y

Benti, F., Diga, G. M., Feyisa, G. L., & Tolesa, A. R. (2022). Modeling coffee (*Coffea arabica* L.) climate suitability under current and future scenario in Jimma zone, Ethiopia. *Environmental Monitoring and Assessment, 194*(4), 271. https://doi.org/10.1007/s10661-022-09895-9

Fick, S. E., & Hijmans, R. J. (2017). WorldClim 2: New 1-km spatial resolution climate surfaces for global land areas. *International Journal of Climatology, 37*(12), 4302–4315. https://doi.org/10.1002/joc.5086

IFPRI. (2019). *Global spatially-disaggregated crop production statistics data for 2010 version 2.0* [Data set]. Harvard Dataverse. https://doi.org/10.7910/DVN/PRFF8V

Jelinski, D. E., & Wu, J. (1996). The modifiable areal unit problem and implications for landscape ecology. *Landscape Ecology, 11*(3), 129–140. https://doi.org/10.1007/BF02447512

King, M., Altdorff, D., Li, P., Galagedara, L., Holden, J., & Unc, A. (2018). Northward shift of the agricultural climate zone under 21st-century global climate change. *Scientific Reports, 8*, 7904. https://doi.org/10.1038/s41598-018-26321-8

MAFF. (2024). *Crop statistics: Rice (Hokkaido and Japan)* [Data set]. Ministry of Agriculture, Forestry and Fisheries of Japan. https://www.maff.go.jp/

Malone, B. P., Kidd, D. B., Minasny, B., & McBratney, A. B. (2015). Taking account of uncertainties in digital land suitability assessment. *PeerJ, 3*, e1366. https://doi.org/10.7717/peerj.1366

Mohamed, A. H., Shendi, M. M., Awadalla, A. A., Mahmoud, A. G., & Semida, W. M. (2019). Land suitability modeling for newly reclaimed area using GIS-based multi-criteria decision analysis. *Environmental Monitoring and Assessment, 191*(9), 535. https://doi.org/10.1007/s10661-019-7649-z

NASA POWER Project. (2025). *Prediction Of Worldwide Energy Resources (POWER), daily point API, version 2* [Data set]. NASA Langley Research Center. https://power.larc.nasa.gov/

Natural Earth. (2024). *Admin 0 – Countries, 1:50m, version 5.1* [Data set]. https://www.naturalearthdata.com/

Ojara, M. A., Yunsheng, L., Ongoma, V., Mumo, L., Akodi, D., Ayugi, B., & Ogwang, B. A. (2021). Projected changes in East African climate and its impacts on climatic suitability of maize production areas by the mid-twenty-first century. *Environmental Monitoring and Assessment, 193*(12), 831. https://doi.org/10.1007/s10661-021-09547-4

Rashidi, F., & Sharifian, S. (2022). A comparative analysis of three multi-criteria decision-making methods for land suitability assessment. *Environmental Monitoring and Assessment, 194*(9), 657. https://doi.org/10.1007/s10661-022-10259-6

Siebert, S., Henrich, V., Frenken, K., & Burke, J. (2013). *Global map of irrigation areas version 5* [Data set]. Rheinische Friedrich-Wilhelms-University and FAO. https://www.fao.org/aquastat/en/geospatial-information/global-maps-irrigated-areas/

Sloat, L. L., Davis, S. J., Gerber, J. S., Moore, F. C., Ray, D. K., West, P. C., & Mueller, N. D. (2020). Climate adaptation by crop migration. *Nature Communications, 11*, 1243. https://doi.org/10.1038/s41467-020-15076-4

Snelder, T., Lilburne, L., Booker, D., Whitehead, A., Harris, S., Larned, S., Semadeni-Davies, A., Plew, D., & McDowell, R. (2023). Land-use suitability is not an intrinsic property of a land parcel. *Environmental Management, 71*(5), 981–997. https://doi.org/10.1007/s00267-022-01764-y

Tenerelli, P., & Carver, S. (2012). Multi-criteria, multi-objective and uncertainty analysis for agro-energy spatial modelling. *Applied Geography, 32*(2), 724–736. https://doi.org/10.1016/j.apgeog.2011.08.013

Van, H. D., Thi, X. A. T., Le Thi, V. L., Van, T. T., Pham, N. T., Phong, N. T., Gagnon, A. S., Pham, Q. B., & Anh, D. T. (2022). Zoning the suitability of the western Mekong Delta for paddy rice cultivation and aquaculture under current and future environmental conditions. *Environmental Monitoring and Assessment, 194*(Suppl. 2), 767. https://doi.org/10.1007/s10661-022-10180-y

Wang, Y., Zhao, J., Zhao, M., Gao, Z., Shi, X., Lu, J., Hao, J., & Chu, Q. (2024). Response of the cultivation suitability of Pu'er tea (*Camellia sinensis* var. *assamica*) to climate conditions and change in China. *Environmental Monitoring and Assessment, 196*(4), 371. https://doi.org/10.1007/s10661-024-12534-0

Xu, E., & Zhang, H. (2013). Spatially-explicit sensitivity analysis for land suitability evaluation. *Applied Geography, 45*, 1–9. https://doi.org/10.1016/j.apgeog.2013.08.005

Yu, Q., You, L., Wood-Sichra, U., Ru, Y., Joglekar, A. K. B., Fritz, S., Xiong, W., Lu, M., Wu, W., & Yang, P. (2020). A cultivated planet in 2010 – Part 2: The global gridded agricultural-production maps. *Earth System Science Data, 12*(4), 3545–3572. https://doi.org/10.5194/essd-12-3545-2020

Zabel, F., Putzenlechner, B., & Mauser, W. (2014). Global agricultural land resources – A high resolution suitability evaluation and its perspectives until 2100 under climate change conditions. *PLoS ONE, 9*(9), e107522. https://doi.org/10.1371/journal.pone.0107522
