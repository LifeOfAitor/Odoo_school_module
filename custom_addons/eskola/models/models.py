from odoo import models, fields, api
import logging
from datetime import date


# Ikasle modeloa, ikaslearen datuak gordeko dira hemen
class EskolaIkasle(models.Model):
    _name = "eskola.ikasle"
    _description = "Eskolako Ikasleak"

    name = fields.Char(string="Izena", required=True)
    surname = fields.Char(string="Abizena", required=True)
    ikasle_age = fields.Integer(string="Adina", compute='_compute_ikasle_age')
    image = fields.Image(string="Argazkia")
    ikasle_day_of_birth = fields.Date(string="Jaiotze data", required=True)
    ikasle_gender = fields.Selection(([("m", "Mutila"), ("e", "Emakumea"), ("b", "Bestea")]), string="Generoa")

    ziklo_id = fields.Many2one("eskola.ziklo", string="Zikloa", required=True, help="Ikaslearen ikasketa zikloa")
    gela_id = fields.Many2one("eskola.gela", string="Gela", required=True, help="Ikaslearen gela")
    ekipo_ids = fields.One2many("eskola.ekipo", "ikasle_id", string="Esleitutako Ekipoa", help="Ikasleari esleitutako ekipoa")   
    falta_ids = fields.One2many("eskola.falta", "ikasle_id", string="Faltak")
    nota_ids = fields.One2many("eskola.nota", "ikasle_id", string="Notak")

    # Ikaslearen adina kalkulatzen du jaiotze data ezarriaren arabera
    @api.depends('ikasle_day_of_birth')
    def _compute_ikasle_age(self):
        for record in self:
            if record.ikasle_day_of_birth:
                today = date.today()
                birth_date = record.ikasle_day_of_birth
                age = today.year - birth_date.year
                if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                    age -= 1
                record.ikasle_age = age
            else:
                record.ikasle_age = 0


# Ziklo modeloa, ikasketa zikloak gordeko dira hemen
class EskolaZiklo(models.Model):
    _name = "eskola.ziklo"
    _description = "Eskola Zikloak"

    name = fields.Char(string="Izena", required=True)
    ikasles_ids = fields.One2many("eskola.ikasle", "ziklo_id", string="Ikasleak")
    ikasgai_ids = fields.One2many("eskola.ikasgai", "ziklo_id", string="Ikasgaiak")


# Gela modeloa, eskola gelak gordeko dira hemen eta gelako ikasleak bai ekipoak lotuko eta erakutsiko dira
class EskolaGela(models.Model):
    _name = "eskola.gela"
    _description = "Eskola Gelak"

    name = fields.Char(string="Izena", required=True)
    ikasle_number = fields.Integer(string="Ikasle Kopurua", compute='_compute_ikasle_number', store=True)

    ikasle_ids = fields.One2many("eskola.ikasle", "gela_id", string="Ikasleak")
    ziklo_id = fields.Many2one("eskola.ziklo", string="Zikloa", required=True, help="Gelaren zikloa")
    location_id = fields.Many2one("stock.location", string="Kokapena", help="Kokalekua ezarria gela hontarako")
    ekipo_ids = fields.One2many("eskola.ekipo", "gela_id", string="Esleitutako Ekipoa", help="Ikasleari esleitutako ekipoa") 

    # Kokaleku ez errepikagarria ziurtatzeko
    _sql_constraints = [
        ('unique_location_id', 'UNIQUE(location_id)', 'Gela bakoitzak bere kokaleku berezia.'),
    ]
    
    # Gelako ikasle kopurua lortzeko
    @api.depends('ikasle_ids')
    def _compute_ikasle_number(self):
        for record in self:
            record.ikasle_number = len(record.ikasle_ids)


# Irakasle modeloa, irakasleen datuak gordeko dira hemen
class EskolaIrakasle(models.Model):
    _name = "eskola.irakasle"
    _description = "Irakasleak"
    
    image = fields.Image(string="Argazkia")
    name = fields.Char(string="Izena", required=True)
    surname = fields.Char(string="Abizena", required=True)
    user_id = fields.Many2one('res.users', string="User") #irakaslea, irakasle horren erabiltzailearekin lotzeko

    # Irakasle berria sortzerakoan edo editatzerakoan irakasle taldean automatikoki sartzeko funtzioak
    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._assign_irakasle_group()
        return record

    def write(self, vals):
        res = super().write(vals)
        if 'user_id' in vals:
            self._assign_irakasle_group()
        return res

    def _assign_irakasle_group(self):
        group = self.env.ref('eskola.group_eskola_irakasle')
        for rec in self:
            if rec.user_id and group not in rec.user_id.group_ids:
                rec.user_id.write({
                    'group_ids': [(4, group.id)]
                })


# Mantenimendu modeloa, mantenimendu langileen datuak gordeko dira hemen
class EskolaMantenimendu(models.Model):
    _name = "eskola.mantenimendu"
    _description = "Mantenimendu"
    
    image = fields.Image(string="Argazkia")
    name = fields.Char(string="Izena", required=True)
    surname = fields.Char(string="Abizena", required=True)
    user_id = fields.Many2one('res.users', string="User") #mantenimendu 'user', mantenimendu horren erabiltzailearekin lotzeko

    # Mantenimendu berria sortzerakoan mantenimendu taldean automatikoki sartzeko
    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._assign_mantenimendu_group()
        return record

    def write(self, vals):
        res = super().write(vals)
        if 'user_id' in vals:
            self._assign_mantenimendu_group()
        return res

    def _assign_mantenimendu_group(self):
        group = self.env.ref('eskola.group_eskola_mantenimendu')
        for rec in self:
            if rec.user_id and group not in rec.user_id.group_ids:
                rec.user_id.write({
                    'group_ids': [(4, group.id)]
                })


# Ekipo modeloa, modelo astuna eta konplexua da, stock mugimenduak kudeatzen dituena
# Ekipoak sortzerakoan, editatzerakoan eta ezabatzekorako stock mugimenduak sortzen ditu, ezarritako gelaren (kokalekuaren) arabera
# Ekipo bakoitza biltegiko produktuekin lotuta dago
class EskolaEkipo(models.Model):
    _name = "eskola.ekipo"
    _description = "Eskola Ekipoa"
    
    name = fields.Char(string="Izena", required=True)
    notes = fields.Text(string="Oharrak")

    product_id = fields.Many2one("product.product", string="Produktua", required=True, help="Product associated with this ekipo")
    gela_id = fields.Many2one("eskola.gela", string="Gela", required=True, help="Ekipo location (class/warehouse location)")
    ikasle_id = fields.Many2one("eskola.ikasle", string="Ikaslea", domain="[('gela_id', '=', gela_id)]", help="Ikasle assigned to this ekipo")
    inzidentzia_ids = fields.One2many("eskola.inzidentzia", "ekipo_id", string="Inzidentziak")

    # Biltegi nagusiaren kokalekua lortzeko funtzio laguntzailea
    def _get_main_warehouse_location(self):
        """Get the WH/Biltegi nagusia location"""
        location = self.env['stock.location'].search([
            ('complete_name', '=', 'WH/Biltegi nagusia')
        ], limit=1)
        if not location:
            # Bilaketa alternatiboa, izen hutsean
            location = self.env['stock.location'].search([
                ('name', '=', 'Biltegi nagusia')
            ], limit=1)
        return location

    # Stock mugimenduak sortzeko funtzio laguntzailea barne mugimenduak kudeatzen dituena
    # Guk ezarritako kokalekuen artean mugimenduak sortzen ditu, produktua eta kantitatea erabiliz eta ezarritako gelako kokalekuaren arabera
    def _create_stock_movement(self, source_location_id, dest_location_id, product_id, quantity=1):
        """Create internal stock movement"""
        picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'internal'),
            ('warehouse_id.name', '=', 'WH')
        ], limit=1)
        
        if not picking_type:
            picking_type = self.env['stock.picking.type'].search([
                ('code', '=', 'internal')
            ], limit=1)

        if not picking_type:
            raise ValueError("No internal picking type found. Please configure warehouse properly.")

        picking_vals = {
            'picking_type_id': picking_type.id,
            'location_id': source_location_id,
            'location_dest_id': dest_location_id,
        }
        picking = self.env['stock.picking'].create(picking_vals)

        # Stock mugimendua sortu
        move_vals = {
            'product_id': product_id,
            'product_uom_qty': quantity,
            'product_uom': self.env.ref('uom.product_uom_unit').id,
            'location_id': source_location_id,
            'location_dest_id': dest_location_id,
            'picking_id': picking.id,
        }
        move = self.env['stock.move'].create(move_vals)
        
        # Mugimendua konfirmatu eta esleitu
        picking.action_confirm()
        picking.action_assign()
        
        # Mugimendua balidatu
        result = picking.button_validate()
        
        # Egoera 'done' ezarri baldin bada, esleitu
        if not result:
            picking.state = 'done'

        return picking

    @api.model
    def create(self, vals):
        """Mugimendua sortu biltegi nagusitik gelara (gelaren kokalekua) ekipoa sortzerakoan"""
        record = super().create(vals)
        
        if record.gela_id and record.gela_id.location_id and record.product_id:
            main_warehouse = record._get_main_warehouse_location()
            if main_warehouse:
                try:
                    record._create_stock_movement(
                        source_location_id=main_warehouse.id,
                        dest_location_id=record.gela_id.location_id.id,
                        product_id=record.product_id.id
                    )
                    logging.info(f"Stock movement created for equipment {record.name} from main warehouse to {record.gela_id.name}")
                except Exception as e:
                    logging.error(f"Error creating stock movement: {e}")
        
        return record

    def write(self, vals):
        """Mugimendua sortu biltegi nagusitik gelara (gelaren kokalekua) ekipoa editatzerakoan, adibidez, gela aldatzerakoan"""
        for record in self:
            old_gela_id = record.gela_id
            
            result = super(EskolaEkipo, record).write(vals)
            
            if 'gela_id' in vals and old_gela_id:
                new_gela = self.env['eskola.gela'].browse(vals['gela_id'])
                
                if old_gela_id.location_id and new_gela.location_id and record.product_id:
                    try:
                        record._create_stock_movement(
                            source_location_id=old_gela_id.location_id.id,
                            dest_location_id=new_gela.location_id.id,
                            product_id=record.product_id.id
                        )
                        logging.info(f"Stock movement created for equipment {record.name} from {old_gela_id.name} to {new_gela.name}")
                    except Exception as e:
                        logging.error(f"Error creating stock movement: {e}")
            
            return result
        
        return super().write(vals)

    def unlink(self):
        """Mugimendua sortu biltegi nagusitik gelara (gelaren kokalekua) ekipoa ezabatzearakoan ekipoa biltegi nagusira itzultzeko"""
        main_warehouse = self._get_main_warehouse_location()
        
        for record in self:
            if record.gela_id and record.gela_id.location_id and record.product_id and main_warehouse:
                try:
                    record._create_stock_movement(
                        source_location_id=record.gela_id.location_id.id,
                        dest_location_id=main_warehouse.id,
                        product_id=record.product_id.id
                    )
                    logging.info(f"Equipment {record.name} returned to main warehouse")
                except Exception as e:
                    logging.error(f"Error returning equipment to main warehouse: {e}")
        
        return super().unlink()


# Falta modeloa, ikasleen faltak gordeko dira hemen, eta ikasle bati egongo da lotuta falta
class EskolaFalta(models.Model):
    _name = "eskola.falta"
    _description = "Ikasleen Faltak"

    date = fields.Date(string="Data", required=True)
    hours = fields.Selection([
        ("1", "Ordu 1"),
        ("2", "2 Ordu"),
        ("3", "3 Ordu"),
        ("4", "4 Ordu"),
        ("5", "5 Ordu"),
        ("6", "6 Ordu")
    ], string="Orduak", required=True)
    motive = fields.Selection([
        ("justifikatua", "Justifikatua"),
        ("justifikatu_gabea", "Justifikatu gabea"),
    ], string="Zergatia", required=True)
    note = fields.Char(string="Oharra")

    ikasle_id = fields.Many2one("eskola.ikasle", string="Ikaslea", required=True)

    # Data + ikasle errepikatzen ez direla ziurtatzeko
    _sql_constraints = [
        (
            'data_ikasle_unique',
            'unique(date, ikasle_id)',
            'Ikasle honek dagoeneko falta bat du zehaztutako datan.'
        )
    ]


# Ikasgai modeloa, ikasgaiak gordeko dira hemen eta ziklo bati lotuta egongo dira
class EskolaIkasgai(models.Model):
    _name = "eskola.ikasgai"
    _description = "Ikasgaiak"

    name = fields.Char(string="Izena", required=True)

    ziklo_id = fields.Many2one("eskola.ziklo", string="Zikloa", required=True)


# Nota modeloa, ikasleen notak gordeko dira hemen, ikasle bati eta ikasgai bati lotuta egongo dira
class EskolaNota(models.Model):
    _name = "eskola.nota"
    _description = "Ikasleen Notak"

    mark = fields.Float(string="Nota", required=True, help="0-10 arteko nota")

    ikasle_id = fields.Many2one("eskola.ikasle", string="Ikaslea", required=True)
    ziklo_id = fields.Many2one("eskola.ziklo", string="Zikloa", related="ikasle_id.ziklo_id", store=True, readonly=True)
    ikasgai_id = fields.Many2one("eskola.ikasgai", string="Ikasgaia", required=True, domain="[('ziklo_id','=',ziklo_id)]")

    # Ikasle + ikasgai errepikatzen ez direla ziurtatzeko
    _nota_ikasle_unique = models.Constraint(
        'unique(ikasle_id, ikasgai_id)',
        'Ezin dira notetan ikasgai errepikatuak egon.',
    )
    # Noten balioa 0 eta 10 artean dagoela ziurtatzeko
    _nota_ikasle_rango = models.Constraint(
        'check(mark >= 0 AND mark <= 10)',
        'Nota 0 eta 10 artean egon behar da.',
    )

# Inzidentzia modeloa, ekipoen inzidentziak gordeko dira hemen, ekipo bati lotuta egongo dira
class EskolaInzidentzia(models.Model):
    _name = "eskola.inzidentzia"
    _description = "Ekipoen Inzidentziak"

    note = fields.Text(string="Oharra", required=True)
    status = fields.Selection([
        ("pending", "Zain"),
        ("done", "Eginda"),
    ], string="Egoera", required=True, default="pending")
    
    ekipo_id = fields.Many2one("eskola.ekipo", string="Ekipoa", required=True)