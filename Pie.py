import random
from random import randint
from streamlit_echarts import JsCode
from streamlit_echarts import st_echarts
from streamlit_echarts import st_pyecharts

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Geo
from pyecharts.charts import Liquid
from pyecharts.charts import Timeline
from pyecharts.charts import WordCloud
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pyecharts.charts import Pie


def main():
    # ST_PAGES = {
    #     "Basic line chart": render_basic_line,
    #     "Basic area chart": render_basic_area,
    #     "Stacked area chart": render_stacked_area,
    #     "Mixed line and bar": render_mixed_line_bar,
    #     "Custom pie chart": render_custom_pie,
    #     "Effect scatter chart": render_effect_scatter,
    #     "Calendar heatmap": render_calendar_heatmap,
    #     "Basic treemap": render_treemap,
    #     "Datazoom": render_datazoom,
    #     "Dataset": render_dataset,
    #     "Map": render_map,
    #     "Click event": render_event,
    #     "Liquidfill": render_liquid,
    #     "Wordcloud": render_wordcloud,
    # }

    PY_ST_PAGES = {
        "Basic bar chart": render_bar_py,
        "Custom themes": render_custom_py,
        "Filter with legend": render_filter_legend_py,
        "Vertical datazoom": render_vertical_datazoom_py,
        "Timeline": render_timeline_py,
        "Chart with randomization": render_randomize_py,
        "JsCode coloring": render_js_py,
        "Map": render_map_py,
        "Liquidfill": render_liquid_py,
        "Wordcloud": render_wordcloud_py,
        "basic Pie Chart": render_basic_pie_chart,
    }

    st.title("Hello ECharts !")
    st.sidebar.header("Configuration")

    select_lang = st.sidebar.selectbox(
        "Choose your preferred API:", ("echarts", "pyecharts", "null")
    )

    if select_lang == "pyecharts":
        page = st.sidebar.selectbox(
            "Choose an example", options=list(PY_ST_PAGES.keys())
        )
        PY_ST_PAGES[page]()


def render_bar_py():
    with st.echo("below"):
        b = (
            Bar()
            .add_xaxis(["Microsoft", "Amazon", "IBM", "Oracle", "Google", "Alibaba"])
            .add_yaxis(
                "2017-2018 Revenue in (billion $)", [21.2, 20.4, 10.3, 6.08, 4, 2.2]
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="Top cloud providers 2018", subtitle="2017-2018 Revenue"
                ),
                toolbox_opts=opts.ToolboxOpts(),
            )
        )
        st_pyecharts(b)


def render_custom_py():
    with st.echo("below"):
        b = (
            Bar()
            .add_xaxis(["Microsoft", "Amazon", "IBM", "Oracle", "Google", "Alibaba"])
            .add_yaxis(
                "2017-2018 Revenue in (billion $)", [21.2, 20.4, 10.3, 6.08, 4, 2.2]
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="Top cloud providers 2018", subtitle="2017-2018 Revenue"
                )
            )
        )
        st_pyecharts(b, theme=ThemeType.DARK)

        st_pyecharts(
            b,
            theme={
                "backgroundColor": "#f4cccc",
                "textStyle": {"color": "rgba(255, 0, 0, 0.8)"},
            },
        )


def render_filter_legend_py():
    with st.echo("below"):
        c = (
            Bar(
                init_opts=opts.InitOpts(
                    animation_opts=opts.AnimationOpts(
                        animation_delay=1000, animation_easing="elasticOut"
                    )
                )
            )
            .add_xaxis(Faker.choose())
            .add_yaxis("商家A", Faker.values())
            .add_yaxis("商家B", Faker.values())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Bar-动画配置基本示例", subtitle="我是副标题")
            )
        )
        st_pyecharts(c)


def render_vertical_datazoom_py():
    with st.echo("below"):
        c = (
            Bar()
            .add_xaxis(Faker.days_attrs)
            .add_yaxis("商家A", Faker.days_values, color=Faker.rand_color())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Bar-DataZoom（slider-垂直）"),
                datazoom_opts=opts.DataZoomOpts(orient="vertical"),
            )
        )
        st_pyecharts(c, height="400px")


def render_timeline_py():
    with st.echo("below"):
        x = Faker.choose()
        tl = Timeline()
        for i in range(2015, 2020):
            bar = (
                Bar()
                .add_xaxis(x)
                .add_yaxis("商家A", Faker.values())
                .add_yaxis("商家B", Faker.values())
                .set_global_opts(title_opts=opts.TitleOpts("某商店{}年营业额".format(i)))
            )
            tl.add(bar, "{}年".format(i))
        st_pyecharts(tl)


def render_randomize_py():
    with st.echo("below"):
        b = (
            Bar()
            .add_xaxis(["Microsoft", "Amazon", "IBM", "Oracle", "Google", "Alibaba"])
            .add_yaxis(
                "2017-2018 Revenue in (billion $)", random.sample(range(100), 10)
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="Top cloud providers 2018", subtitle="2017-2018 Revenue"
                ),
                toolbox_opts=opts.ToolboxOpts(),
            )
        )
        st_pyecharts(
            b, key="echarts"
        )  # Add key argument to not remount component at every Streamlit run
        st.button("Randomize data")


def render_js_py():
    with st.echo("below"):
        st.markdown(
            """Overwrite chart colors with JS. 
        Under 50 : red. Between 50 - 100 : blue. Over 100 : green"""
        )
        color_function = """
                function (params) {
                    if (params.value > 0 && params.value < 50) {
                        return 'red';
                    } else if (params.value > 50 && params.value < 100) {
                        return 'blue';
                    }
                    return 'green';
                }
                """
        c = (
            Bar()
            .add_xaxis(Faker.choose())
            .add_yaxis(
                "商家A",
                Faker.values(),
                itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)),
            )
            .add_yaxis(
                "商家B",
                Faker.values(),
                itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)),
            )
            .add_yaxis(
                "商家C",
                Faker.values(),
                itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)),
            )
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar-自定义柱状颜色"))
        )
        st_pyecharts(c)


def render_map_py():
    with st.echo("below"):
        g = (
            Geo()
            .add_schema(maptype="china")
            .add("geo", [list(z) for z in zip(Faker.provinces, Faker.values())])
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(),
                title_opts=opts.TitleOpts(title="Geo-基本示例"),
            )
        )
        st_pyecharts(g)


def render_liquid_py():
    with st.echo("below"):
        c = (
            Liquid()
            .add("lq", [0.6, 0.7])
            .set_global_opts(title_opts=opts.TitleOpts(title="Liquid-基本示例"))
        )
        st_pyecharts(c)


def render_wordcloud_py():
    with st.echo("below"):
        data = [
            ("生活资源", "999"),
            ("供热管理", "888"),
            ("供气质量", "777"),
            ("生活用水管理", "688"),
            ("一次供水问题", "588"),
            ("交通运输", "516"),
            ("城市交通", "515"),
            ("环境保护", "483"),
            ("房地产管理", "462"),
            ("城乡建设", "449"),
            ("社会保障与福利", "429"),
            ("社会保障", "407"),
            ("文体与教育管理", "406"),
            ("公共安全", "406"),
            ("公交运输管理", "386"),
            ("出租车运营管理", "385"),
            ("供热管理", "375"),
            ("市容环卫", "355"),
            ("自然资源管理", "355"),
            ("粉尘污染", "335"),
            ("噪声污染", "324"),
            ("土地资源管理", "304"),
            ("物业服务与管理", "304"),
            ("医疗卫生", "284"),
            ("粉煤灰污染", "284"),
            ("占道", "284"),
            ("供热发展", "254"),
            ("农村土地规划管理", "254"),
            ("生活噪音", "253"),
            ("供热单位影响", "253"),
            ("城市供电", "223"),
            ("房屋质量与安全", "223"),
            ("大气污染", "223"),
            ("房屋安全", "223"),
            ("文化活动", "223"),
            ("拆迁管理", "223"),
            ("公共设施", "223"),
            ("供气质量", "223"),
            ("供电管理", "223"),
            ("燃气管理", "152"),
            ("教育管理", "152"),
            ("医疗纠纷", "152"),
            ("执法监督", "152"),
            ("设备安全", "152"),
            ("政务建设", "152"),
            ("县区、开发区", "152"),
            ("宏观经济", "152"),
            ("教育管理", "112"),
            ("社会保障", "112"),
            ("生活用水管理", "112"),
            ("物业服务与管理", "112"),
            ("分类列表", "112"),
            ("农业生产", "112"),
            ("二次供水问题", "112"),
            ("城市公共设施", "92"),
            ("拆迁政策咨询", "92"),
            ("物业服务", "92"),
            ("物业管理", "92"),
            ("社会保障保险管理", "92"),
            ("低保管理", "92"),
            ("文娱市场管理", "72"),
            ("城市交通秩序管理", "72"),
            ("执法争议", "72"),
            ("商业烟尘污染", "72"),
            ("占道堆放", "71"),
            ("地上设施", "71"),
            ("水质", "71"),
            ("无水", "71"),
            ("供热单位影响", "71"),
            ("人行道管理", "71"),
            ("主网原因", "71"),
            ("集中供热", "71"),
            ("客运管理", "71"),
            ("国有公交（大巴）管理", "71"),
            ("工业粉尘污染", "71"),
            ("治安案件", "71"),
            ("压力容器安全", "71"),
            ("身份证管理", "71"),
            ("群众健身", "41"),
            ("工业排放污染", "41"),
            ("破坏森林资源", "41"),
            ("市场收费", "41"),
            ("生产资金", "41"),
            ("生产噪声", "41"),
            ("农村低保", "41"),
            ("劳动争议", "41"),
            ("劳动合同争议", "41"),
            ("劳动报酬与福利", "41"),
            ("医疗事故", "21"),
            ("停供", "21"),
            ("基础教育", "21"),
            ("职业教育", "21"),
            ("物业资质管理", "21"),
            ("拆迁补偿", "21"),
            ("设施维护", "21"),
            ("市场外溢", "11"),
            ("占道经营", "11"),
            ("树木管理", "11"),
            ("农村基础设施", "11"),
            ("无水", "11"),
            ("供气质量", "11"),
            ("停气", "11"),
            ("市政府工作部门（含部门管理机构、直属单位）", "11"),
            ("燃气管理", "11"),
            ("市容环卫", "11"),
            ("新闻传媒", "11"),
            ("人才招聘", "11"),
            ("市场环境", "11"),
            ("行政事业收费", "11"),
            ("食品安全与卫生", "11"),
            ("城市交通", "11"),
            ("房地产开发", "11"),
            ("房屋配套问题", "11"),
            ("物业服务", "11"),
            ("物业管理", "11"),
            ("占道", "11"),
            ("园林绿化", "11"),
            ("户籍管理及身份证", "11"),
            ("公交运输管理", "11"),
            ("公路（水路）交通", "11"),
            ("房屋与图纸不符", "11"),
            ("有线电视", "11"),
            ("社会治安", "11"),
            ("林业资源", "11"),
            ("其他行政事业收费", "11"),
            ("经营性收费", "11"),
            ("食品安全与卫生", "11"),
            ("体育活动", "11"),
            ("有线电视安装及调试维护", "11"),
            ("低保管理", "11"),
            ("劳动争议", "11"),
            ("社会福利及事务", "11"),
            ("一次供水问题", "11"),
        ]

        c = (
            WordCloud()
            .add(series_name="热点分析", data_pair=data, word_size_range=[6, 66])
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="热点分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                ),
                tooltip_opts=opts.TooltipOpts(is_show=True),
            )
        )
        st_pyecharts(c)


def render_basic_pie_chart():
    data = [
        ("生活资源", "999"),
        ("供热管理", "888"),
        ("供气质量", "777"),
        ("生活用水管理", "688"),
        ("一次供水问题", "588"),
        ("交通运输", "516"),
        ("城市交通", "515"),
        ("环境保护", "483"),
        ("房地产管理", "462"),
        ("城乡建设", "449"),
        ("社会保障与福利", "429"),
        ("社会保障", "407"),
        ("文体与教育管理", "406"),
        ("公共安全", "406"),
        ("公交运输管理", "386"),
        ("出租车运营管理", "385"),
        ("供热管理", "375"),
        ("市容环卫", "355"),
        ("自然资源管理", "355"),
        ("粉尘污染", "335"),
        ("噪声污染", "324"),
        ("土地资源管理", "304"),
        ("物业服务与管理", "304"),
        ("医疗卫生", "284"),
        ("粉煤灰污染", "284"),
        ("占道", "284"),
        ("供热发展", "254"),
        ("农村土地规划管理", "254"),
        ("生活噪音", "253"),
        ("供热单位影响", "253"),
        ("城市供电", "223"),
        ("房屋质量与安全", "223"),
        ("大气污染", "223"),
        ("房屋安全", "223"),
        ("文化活动", "223"),
        ("拆迁管理", "223"),
        ("公共设施", "223"),
        ("供气质量", "223"),
        ("供电管理", "223"),
        ("燃气管理", "152"),
        ("教育管理", "152"),
        ("医疗纠纷", "152"),
        ("执法监督", "152"),
        ("设备安全", "152"),
        ("政务建设", "152"),
        ("县区、开发区", "152"),
        ("宏观经济", "152"),
        ("教育管理", "112"),
        ("社会保障", "112"),
        ("生活用水管理", "112"),
        ("物业服务与管理", "112"),
        ("分类列表", "112"),
        ("农业生产", "112"),
        ("二次供水问题", "112")
    ]
    c = (
        Pie()
        .add(series_name="Contoh", data_pair=data)
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-After"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    st_pyecharts(c)


if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Echarts Demo", page_icon=":tada:")
    main()
