def getContentHTML(json):
    html = ""
    for el in json:
        if el["type"] == "text":
            html += f"""
            <div>
                <h1>{el['header']}</h1>
                <p>
                    {el['body']}
                </p>
            </div>
            """
        elif el["type"] == "pricing table":
            inner = ""
            for table in el["body"]:
                inner_inc = ""
                for inc in table["inc"]:
                    inner_inc += f"""
                    <li>
                        <span class="fa-li"><i class="fas fa-check"></i></span>{inc}
                    </li>
                    """
                inner+=f"""
                <div class="col-lg-6">
                    <div class="card mb-5 mb-lg-0">
                        <div class="card-body">
                            <h5 class="card-title text-muted text-uppercase text-center">{table['title']}</h5>
                            <h6 class="card-price text-center">${table['price']}<span class="period">/month</span></h6>
                            <hr />
                            <ul class="fa-ul">
                                {inner_inc}
                            </ul>
                            <a href="{table['goto']}" class="btn btn-block btn-primary text-uppercase">Button</a>
                        </div>
                    </div>
                </div>
                """
            html+=f"""
            <div>
                <h1>{el['header']}</h1>
                    <section class="pricing py-5">
                        <div class="container">
                            <div class="row">
                                {inner}
                            </div>
                        </div>
                    </section>
                </div>
            """
        elif el["type"] == "card":
            inner = ""
            for card in el["body"]:
                inner += f"""
                <div class="col-md-4">
                    <div class="card spec-card">
                        <img class="card-img-top" src="{card['image']}" alt="cardIcon" />
                        <div class="card-body"><p class="card-text">{card['title']}</p></div>
                    </div>
                </div>
                """
            html += f"""
            <div>
                <h1>{el['header']}</h1>
                <div class="cards-div">
                    <div class="card-block">
                        {inner}
                    </div>
                </div>
            </div>
            """
    return html
