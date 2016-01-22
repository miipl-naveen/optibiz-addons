from openerp.osv import osv,fields

class store_default_values(osv.osv):
    _name= 'store.default.values'
    _columns = {

        'price_expiry_days':fields.integer('Price Expiry Days'),

    }

    _defaults = {
        'price_expiry_days': 0
    }

store_default_values()

class sale_config_settings(osv.osv_memory):
    _name = 'sale.config.settings'
    _inherit = 'sale.config.settings'
    _columns = {
    'product_price_expiry_in_days': fields.integer('Product price expires in ',default=10),
    }

    _defaults = {
        'product_price_expiry_in_days': 0
    }

    def get_default_product_price_expiry_in_days(self, cr, uid, fields, context=None):

        price_expiry_in_days = 0
        idlist=self.pool.get('store.default.values').search(cr, uid, [], context=context)
        print idlist,len(idlist)
        if idlist:
            for record in self.pool.get('store.default.values').browse(cr, uid, idlist, context=context):
                #print [record.id]['price_expiry_days']
                price_expiry_in_days=record.price_expiry_days
        if price_expiry_in_days:
            return {'product_price_expiry_in_days': price_expiry_in_days}
        else:
            return {'product_price_expiry_in_days': 10}

    def set_default_product_price_expiry_in_days(self, cr, uid, ids, context=None):
        price_expiry= self.browse(cr, uid, ids[0], context)
        Product_price_expiry=price_expiry.product_price_expiry_in_days
        print Product_price_expiry
        idlist=self.pool.get('store.default.values').search(cr, uid, [], context=context)
        if len(idlist)>0:
            for record in self.pool.get('store.default.values').browse(cr, uid, idlist, context=context):
                i=record.id
            a=self.pool.get('store.default.values').write(cr,uid,i,{'price_expiry_days':Product_price_expiry})
        else:
            vals={}
            vals['price_expiry_days']=Product_price_expiry
            a=self.pool.get('store.default.values').create(cr,uid,vals,context)