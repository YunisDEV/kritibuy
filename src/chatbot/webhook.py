from ..db import session, User, Order, ServerError, Permission
from .utils import getCompany
from ..email import send_mail
from ..dashboard.business_panel import business_data_get
webhook_placeholder = {
    "fulfillmentMessages": [
        {
            "text": {
                "text": [
                    'OK'
                ]
            }
        }
    ]
}


def order_to_company(data):
    response = None
    try:
        print(
            f'Ordering: {data.parameters.get("product")} ---> {data.parameters.get("company")} by {data.user_id}'
        )
        try:
            user = session.query(User).filter(
                User.id == int(data.user_id)).one()
            if not user:
                raise Exception()
        except Exception as e:
            raise Exception('User not found with id: '+data.user_id, 15)
        try:
            company = getCompany(data.parameters.get("company"))
        except Exception as e:
            print('Errorr'+str(e))
            raise Exception('Company not found with brandName: ' +
                            data.parameters.get("company"), 12)
        if not data.parameters.get("product") in company.brandProductTypes:
            response = "This company has not added this product to their service list. But we sent your order. They will contact you soon."
        try:
            order = Order(
                orderedTo=company.id,
                orderedBy=user.id,
                orderedProduct=data.parameters.get("product"),
                orderText=data.query_text
            )
            session.add(order)
            session.commit()
            send_mail(
                Subject='Kritibuy - New Order',
                To=company.email,
                Template={"name":'email_invoice',"data":business_data_get["invoice"](order.id)})
        except Exception as e:
            raise Exception('Order can not be created', 18)
        if not response:
            response = 'Ordered Successfully'
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            response
                        ]
                    }
                }
            ]
        }
    except Exception as e:
        e = tuple(e.args)
        print(e)
        error = ServerError(
            where='Webhook',
            errorCode=e[1],
            errorDesc=e[0],
        )
        session.add(error)
        session.commit()
        response = error.errorDesc+'. Error ID: ' + str(error.id)
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            response
                        ]
                    }
                }
            ]
        }


def get_companies_by_product(data):
    response = None
    companies = []
    print('a')
    try:
        productName = data.parameters.get('product')
        if productName:
            print(productName)
            companies = session.query(User).filter(
                User.brandProductTypes.any(productName)
            ).all()

            businessPermissionId = session.query(Permission).filter(
                Permission.name == 'Business').one().id
            print(companies)
            companies = [
                company.brandName for company in companies if company.permission == businessPermissionId and (company.active == True and company.confirmed == True)]
            if len(companies) == 0:
                raise Exception(
                    'We could not find any company that serve such product')
            else:
                response = ", ".join(companies) + ' serve this product'
        else:
            raise Exception('Please query with a product name.')
    except Exception as e:
        print(e)
        response = str(e)
        session.rollback()
    return {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        response
                    ]
                }
            }
        ]
    }


webhook = {
    "Order to company": order_to_company,
    "Get companies that serve such product": get_companies_by_product
}
