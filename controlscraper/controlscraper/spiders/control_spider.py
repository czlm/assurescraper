import scrapy

class ControlsSpider(scrapy.Spider):
    name = "controls"

    def start_requests(self):
        page = getattr(self, 'page', None)
        if not page:
            raise ValueError("You must specify the page parameter using -a page=<page_prefix>")

        url = f"https://info.standards.tech.gov.sg/control-catalog/{page}/"
        yield scrapy.Request(url=url.strip(), callback=self.parse)

    def parse(self, response):
        page = getattr(self, 'page', None)
        sections = response.css(f"h2[id^='{page}-']")  # Select all h2 elements with id starting with the page prefix
        for section in sections:
            section_id = section.css("::attr(id)").get()
            section_title = section.css("::text").get()

            control_statement = section.xpath("following-sibling::h3[contains(@id, 'control-statement')]/following-sibling::p[1]/text()").get()
            control_recommendations = section.xpath("following-sibling::h3[contains(@id, 'control-recommendations')]/following-sibling::p[1]/text()").get()
            risk_statement = section.xpath("following-sibling::h3[contains(@id, 'risk-statement')]/following-sibling::p[1]/text()").get()
            
            # Check for the presence of parameters
            parameters_present = bool(section.xpath("following-sibling::table//tbody/tr"))

            yield {
                "section_id": section_id,
                "section_title": section_title,
                "control_statement": control_statement,
                "control_recommendations": control_recommendations,
                "risk_statement": risk_statement,
                "parameters_present": parameters_present
            }
