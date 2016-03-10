from openerp.osv import fields, osv
from datetime import date

class miipl_price_update(osv.TransientModel):
    _name = 'miipl.price.update'
    _description = "Product Price Update"
    _columns = {
            'request_id':fields.many2one('miipl.product.requisition', 'Request ID', required=False),
            'product_id': fields.many2one('product.template', 'Product', domain=[('sale_ok', '=', True)], readonly=True,),
            'cost': fields.float('Cost Price',readonly=True),
            'product_purchase_history':fields.one2many('miipl.product.purchase.history', 'miipl_request_id1','Purchase History',limit="2",readonly=True),
            'supplier_line': fields.one2many('miipl.supplier', 'miipl_request_id', 'Supplier Cost Price'),
            'product_supplier_line':fields.one2many('miipl.product.supplier', 'miipl_request_id2','Previous Suppliers',limit="2",readonly=True),

    }


    
    def default_get(self, cr, uid, fields, context=None):
        if context == None:
            context = {}
        request_id = context.get('active_id', [])
        product_id=self.pool.get('miipl.product.requisition').browse(cr,uid,request_id,context).product_id
        p_id=self.pool.get('product.product').search(cr,uid,[('product_tmpl_id','=',product_id.id)])
        po_lines=self.pool.get('purchase.order.line').search(cr,uid,[('product_id','=',p_id[0]),('state','in',('confirmed','done'))],order='create_date desc',limit=15)
        purchase_price_history=[]
        for pol in po_lines:
            pol_id=self.pool.get('purchase.order.line').browse(cr,uid,pol,context)
            temp=[0,False,{'purchase_order_id':pol_id.order_id.id,'product_id':p_id[0],'partner_id':pol_id.partner_id.id,'price_unit':pol_id.price_unit,'po_date':pol_id.create_date}]
            purchase_price_history.append(temp)
        sup_list=[]

        cr.execute("select distinct on (partner_id) partner_id,price_unit,create_date,order_id from purchase_order_line where product_id = "+str(p_id[0])+" and state in ('confirmed','done') order by partner_id, create_date desc")
        for sup in cr.fetchall():
            temp=[0,False,{'purchase_order_id':sup[3],'product_id':p_id[0],'partner_id':sup[0],'price_unit':sup[1],'po_date':sup[2]}]
            sup_list.append(temp)
        return {'request_id': request_id,'product_id':product_id.id,'cost':product_id.standard_price,'product_purchase_history':purchase_price_history,'product_supplier_line':sup_list}
    
    def post_comments(self, cr, uid, id, context=None):
        if context == None:
            context = {}

        for user in self.browse(cr, uid, id, context=context):
            if not user.supplier_line:
                raise osv.except_osv(('Warning!'),("Cannot update Product with out a Supplier."))
            price=100000000000
            for supplier in user.supplier_line:
                supplier_ids = self.pool.get('product.supplierinfo').search(cr,uid,[('product_tmpl_id','=',user.product_id.id)])
                flag=0
                for s_id in supplier_ids:
                    s_id = self.pool.get('product.supplierinfo').browse(cr,uid,s_id,context)
                    if supplier.name.id == s_id.name.id:
                        flag = 1
                        break
                    else:
                        flag = 0
                if flag==1:
                    self.pool.get('product.supplierinfo').write(cr,uid,s_id.id,{'cost':supplier.supplier_cost})
                else:
                    self.pool.get('product.supplierinfo').create(cr,uid,{'name':supplier.name.id,'min_qty':1,'delay':1,'cost':supplier.supplier_cost,'product_tmpl_id':user.product_id.id},context)

                if supplier.supplier_cost < price:
                    price=supplier.supplier_cost
            if user.supplier_line:
                self.write(cr,uid,id,{'cost':price})
                self.pool.get('product.template').write(cr,uid,user.product_id.id,{})
            self.pool.get('miipl.product.requisition').action_cost_price_updated(cr, uid,  user.request_id.id, context)

miipl_price_update()



class miipl_supplier(osv.TransientModel):
    _name = 'miipl.supplier'
    _description = "Product Supplier"
    _columns = {
            'miipl_request_id' : fields.many2one('miipl.price.update', 'Request Id', required=True, ondelete='cascade', select=True),
            'name': fields.many2one('res.partner', 'Supplier', required=True,domain = [('supplier','=',True)], ondelete='cascade', help="Supplier of this product"),
            'supplier_cost': fields.float('Cost Price'),
    }
miipl_price_update()

class miipl_product_purchase_history(osv.TransientModel):
    _name = 'miipl.product.purchase.history'
    _description = "Product Purchase History"
    _columns = {
            'miipl_request_id1' : fields.many2one('miipl.price.update', 'Request Id', required=True, ondelete='cascade', select=True),
            'product_id': fields.many2one('product.product', 'Product', domain=[('purchase_ok','=',True)], change_default=True),
            'partner_id': fields.many2one('res.partner', 'Supplier'),
            'price_unit': fields.float('Unit Price', required=True, ),
            'po_date': fields.datetime('Created Date'),
            'purchase_order_id':fields.many2one('purchase.order','Purchase Order'),


    }
miipl_product_purchase_history()

class miipl_product_supplier(osv.TransientModel):
    _name = 'miipl.product.supplier'
    _description = "Product Supplier"
    _columns = {
            'miipl_request_id2' : fields.many2one('miipl.price.update', 'Request Id', required=True, ondelete='cascade', select=True),
            'product_id': fields.many2one('product.product', 'Product', domain=[('purchase_ok','=',True)], change_default=True),
            'partner_id': fields.many2one('res.partner', 'Supplier'),
            'price_unit': fields.float('Unit Price', required=True, ),
            'po_date': fields.datetime('Created Date'),
            'purchase_order_id':fields.many2one('purchase.order','Purchase Order'),


    }
miipl_product_supplier()



class miipl_sale_price_update(osv.TransientModel):
    _name = 'miipl.sale.price.update'
    _description = "Product Price Update"
    _columns = {
            'price_expiry':fields.float('Price Expires', required=True),
            'request_id':fields.many2one('miipl.product.requisition', 'Request ID', required=False),
            'product_id': fields.many2one('product.template', 'Product', domain=[('sale_ok', '=', True)], readonly=True,),
            'cost': fields.float('Cost Price',readonly=True),
            'sale': fields.float('Sale Price'),
            'coordinator_selling_price': fields.float('Coordinator Price', help="This is the price beyond which the sales person cannot give discounts"),
            'selling_price': fields.float('Executive Price',  help="This is the price beyond which the sales person cannot give discounts"),
            'min_selling_price': fields.float('Manager Price', help="This is the price beyond which the sales manager cannot give discounts"),

    }



    def default_get(self, cr, uid, fields, context=None):
        if context == None:
            context = {}
        request_id = context.get('active_id', [])
        product_id=self.pool.get('miipl.product.requisition').browse(cr,uid,request_id,context).product_id
        return {'request_id': request_id,'product_id':product_id.id,'cost':product_id.standard_price,'sale':product_id.list_price,'coordinator_selling_price':product_id.coordinator_selling_price,'selling_price':product_id.selling_price,'min_selling_price':product_id.min_selling_price,'price_expiry':product_id.price_expiry}

    def post_comments(self, cr, uid, id, context=None):
        if context == None:
            context = {}

        for user in self.browse(cr, uid, id, context=context):
            self.pool.get('product.template').write(cr,uid,user.product_id.id,{'list_price':user.sale,'coordinator_selling_price':user.coordinator_selling_price,'selling_price':user.selling_price,'min_selling_price':user.min_selling_price,'price_expiry':user.price_expiry})
            self.pool.get('miipl.product.requisition').action_done(cr, uid,  user.request_id.id, context)

miipl_sale_price_update()
