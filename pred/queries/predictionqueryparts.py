from pred.queries.querybuilder import QueryPart


def _query_part(sql):
    return QueryPart(sql, [])


def set_search_path(schema):
    return QueryPart("SET search_path TO %s,public;", [schema])


def custom_range_list_query(list_id, model_name):
    return QueryPart("""select '' as name,
'range' || seq as common_name,
max(custom_range_list.chrom) as chrom,
'' as strand,
'' as gene_begin,
case WHEN max(value) > abs(min(value)) THEN
  round(max(value), 4)
ELSE
  round(min(value), 4)
end as max_value,
json_agg(json_build_object('value', round(value, 4), 'start', start_range, 'end', end_range)) as pred,
max(lower(custom_range_list.range)) as range_start,
max(upper(custom_range_list.range)) as range_end
from custom_range_list
left outer join prediction
on prediction.chrom = custom_range_list.chrom
and custom_range_list.range && prediction.range
and model_name = %s
where
custom_range_list.id = %s
group by seq""", [model_name, list_id])


def select_prediction_values():
    return _query_part("""select
common_name,
string_agg(name, '; ') as name,
case WHEN max(value) > abs(min(value)) THEN
  round(max(value), 4)
ELSE
  round(min(value), 4)
end as max_value,
chrom,
strand,
gene_begin,
json_agg(json_build_object('value', round(value, 4), 'start', start_range, 'end', end_range)) as pred
from gene_prediction""")


def name_in_max_prediction_names():
    return _query_part("and common_name in (select common_name from max_prediction_names)")


def filter_gene_list(gene_list, model_name, upstream, downstream):
    """
    Overlapping range filter.
    SQL Explanation:
    The end of the prediction must come after the start of the gene
    and the end of the gene must come after the start of the prediction.
    http://nedbatchelder.com/blog/201310/range_overlap_in_two_compares.html
    """
    return QueryPart("""gene_list = %s
and
model_name = %s
and
case strand when '+' then
  (gene_begin + %s) >= start_range and end_range >= (gene_begin - %s)
else
  (gene_begin + %s) >= start_range and end_range >= (gene_begin - %s)
end""", [gene_list, model_name, downstream, upstream, upstream, downstream])


def filter_common_name(custom_list_id, custom_list_filter, custom_gene_name_type, model_name, upstream, downstream):
    """
    Overlapping range filter.
    SQL Explanation:
    The end of the prediction must come after the start of the gene
    and the end of the gene must come after the start of the prediction.
    http://nedbatchelder.com/blog/201310/range_overlap_in_two_compares.html
    """
    if custom_list_filter.strip().upper() == "ALL":
        custom_list_filter = ""

    inner_filter = "upper(name) in (select upper(gene_name) from custom_gene_list where id = %s)"
    if custom_gene_name_type:
        inner_filter = "upper(common_name) in (select upper(gene_name) from custom_gene_list where id = %s)"

    base_sql = """( common_name in
(select common_name from gene where
    {}))
and
model_name = %s
and
case strand when '+' then
  (gene_begin + %s) >= start_range and end_range >= (gene_begin - %s)
else
  (gene_begin + %s) >= start_range and end_range >= (gene_begin - %s)
end""".format(inner_filter)
    sql = base_sql
    params = [custom_list_id, model_name, upstream, downstream, downstream, upstream]
    if custom_list_filter:
        sql = "gene_list = %s\nand\n{}".format(base_sql)
        params.insert(0, custom_list_filter)
    if not custom_gene_name_type:
        sql += " and " + inner_filter
        params.append(custom_list_id)

    return QueryPart(sql, params)


def items_not_in_gene_list(list_id, gene_list_filter, custom_gene_name_type):
    inner_filter = "upper(gene.name) = upper(custom_gene_list.gene_name)"
    if custom_gene_name_type:
        inner_filter = "upper(gene.common_name) = upper(custom_gene_list.gene_name)"
    sql = """select gene_name from custom_gene_list
where id = %s and not exists
(select 1 from gene where ({})""".format(inner_filter)
    params = [list_id]
    if gene_list_filter and gene_list_filter.upper() != "ALL":
        sql += "and gene_list = %s"
        params.append(gene_list_filter)
    sql += ")"
    return QueryPart(sql, params)


def with_max_prediction_names():
    return _query_part("""with max_prediction_names as (
 select common_name from gene_prediction""")


def end_with():
    return _query_part(")")


def where():
    return _query_part("where")


def value_greater_than(value):
    return QueryPart("and abs(value) > %s", [value])


def group_by_name():
    return _query_part("group by name")


def group_by_common_name_and_parts():
    return _query_part("group by common_name, chrom, strand, gene_begin")


def order_by_chrom_and_txstart():
    return _query_part("order by chrom, gene_begin")


def order_by_name():
    return _query_part("order by name")


def order_by_common_name():
    return _query_part("order by common_name")


def order_by_common_name_and_name():
    return _query_part("order by common_name, name")


def order_by_chrom_txstart():
    return _query_part("order by chrom, txstart")


def order_by_seq():
    return _query_part("order by seq")


def order_by_max_value_desc():
    return _query_part("order by max(abs(value)) desc")


def order_by_max_value_desc_common_name():
    return _query_part("order by max(abs(value)) desc, common_name")


def limit_and_offset(limit, offset):
    return QueryPart("limit %s offset %s", [limit, offset])


def begin_count():
    return _query_part("select count(*) from (")


def end_count():
    return _query_part(") as foo")


def begin():
    return _query_part("begin;")


def commit():
    return _query_part(";commit;")