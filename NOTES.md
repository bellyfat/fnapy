# Cookbook


## Process

You start creating offers in your catalog with the `update_offers` service.
The returned response contains a `batch_id` that allows you to check
the status of your offers.

When you finished updating your offers, you can check if they were actually
created with the `offers_query` service.

Now that you have offers in your catalog, you can retrieve the orders with the
`orders_query` service. 

In order to update the orders (accept, refuse or ship it) you have to use the
`orders_update` service with the `order_id` and the selected action.


## Offers update

* Description 

This service is used to manage your catalog. It allows you to add, update or delete offers.

* Process

1. A valid authentification token is needed.
2. The partner sends a list of offers to add, update or delete.
3. The service returns a batch identifier. With that id you can retrieve the
   process report of the sent feed by using _Batch Status_

* Limitation 

The recommended number of offers to update at once is 10 000. The service
doesn't provide a "purge and replace" mode. To delete offers, you have to use
the <treatment> element on each offer to remove.


### Creation of an offer

We need 5 mandatory parameters:

* a product reference (such as EAN)
* a seller offer reference (such as SKU)
* a product state
* a price
* a quantity

and 3 optional parameters:

* a description of the product
* a showcase number (the position of the offer in the showcase)
* an internal comment visible only by yourself in the seller account


## batch_status

The status of the request is accessed with a batch id. You can use this id to
know the processing status of the request.

* Description 

Presents the status of the last operation. More details are available in the
sub levels presenting errors

* Restriction
    - Extends: xs:string
    - Enumeration:
        – RUNNING: Process is still running
        – OK: Process finished without any error or warning
        – WARNING: Process finished with at least a warning and no error
        – ERROR: Process finished with at least an error, but no blocking error was encountered
        – FATAL: A fatal error occured while processing, the process was not
          done completely or even completely aborted


## offers_query

* Description

This is service is used to retrieve offers from your shop catalog according to
submitted criteria.

* Process

1. A valid authentification token is needed.
2. The partner calls the service with criteria.
3. The service returns the selected offers.

* Limitation

Query is limited to 10 000 offers per call. Above this limit, an error will be
thrown in the response.


## orders_query

## orders_update

* Description

This is service is used to update the status of your orders (accepting,
shipping or updating shipping information).

* Process

1. A valid authentification token is needed.
2. The partners calls the service by sending list of orders and the action to
   make on the related order details (accept, refuse, etc.).
3. The service returns a report of the update processing.

* Limitation

You can update up to 25 orders at once.


Orders statuses follow this workflow:

1. Created
2. Accepted
3. ToShip
4. Shipped
5. Received


## order_update_action

* Description

Defines the actions available on an order from the seller's side

* Restriction

Enumerate:
    - accept_order: The action for the order is accepting orders by the seller
    - confirm_to_send: The action for the order is confirming sending orders by the seller
    - update: The action for the order is updating orders by the seller
    - accept_all_orders: The action for the order is accepting or refusing all order_details of the order by the seller
    - confirm_all_to_send: The action for the order is confirming sending all order_details by the seller
    - update_all: The action for the order is to update tracking information for all order_details


## pricing_query

* Description

Compare price between all marketplace shop and fnac for a specific product.

* Process

    A valid authentification token is needed.
    The partner calls service with a list of product reference
    The service returns for each product reference a list of the lowest prices
    suggested by Fnac Marketplace sellers.

The number of product references to request is limited to 10.

