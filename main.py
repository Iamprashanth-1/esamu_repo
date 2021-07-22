from fastapi import FastAPI
import json

app=FastAPI()
@app.get('/items/{order_id}')
async def root(order_id): 
    order_id=json.loads(order_id) 
    distance_prices={5000:[0,10000],10000:[10000,20000],20000:[20000,50000],100000:[50000,100000]}
    item_total=0
    ords=order_id["order_items"]
    for items in order_id.get("order_items"):
        price,distance_range=items.get('quantity'),items.get('price')
        item_total+=price*distance_range
    dist=order_id.get('distance')
    for key,val in distance_prices.items():
        if val[0]<=dist<val[1]:
            total_delivery_price=key
            break
    total_order=total_delivery_price+item_total
    try:
        offer=order_id.get('offer')
        if offer.get('offer_type')=='FLAT':
            discount=min(offer.get('offer_val'),total_order)
        else:
            discount=total_delivery_price
    except:
        discount=0
        
    final_price=total_order-discount

    return {"order_total":final_price}