from odoo import models, fields, api
import logging

# Ikaslearen egitura hemen prestatuko dugu
class EskolaIkasleak(models.Model):
    _name = "eskola.ikasleak"
    _description = "Eskolako Ikasleak"

    name = fields.Char(string="Izena", required=True)
    surname = fields.Char(string="Abizena", required=True)
    student_age = fields.Integer(string="Adina", required=True)
    image = fields.Image(string="Argazkia")
    student_day_of_birth = fields.Date(string="Jaiotze data", required=True)
    student_gender = fields.Selection(([("m", "Mutila"), ("e", "Emakumea"), ("b", "Bestea")]), string="Generoa")
    cycle_id = fields.Many2one("eskola.cycle", string="Zikloa", required=True, help="Ikaslearen ikasketa zikloa")
    class_id = fields.Many2one("eskola.class", string="Gela", required=True, help="Ikaslearen gela")
    equipment_ids = fields.One2many(
        "eskola.equipment",
        "student_id",
        string="Esleitutako Ekipoa",
        help="Ikasleari esleitutako ekipoa"
    )   
    attendance_ids = fields.One2many(
        "eskola.attendance",
        "student_id",
        string="Asistentziak"
    )
    grade_ids = fields.One2many(
        "eskola.grade",
        "student_id",
        string="Notak"
    )


class EskolaCycle(models.Model):
    _name = "eskola.cycle"
    _description = "Eskola Zikloak"

    name = fields.Char(string="Izena", required=True)
    students_ids = fields.One2many(
        "eskola.ikasleak",
        "cycle_id",
        string="Ikasleak"
    )
    subject_ids = fields.One2many(
        "eskola.subject",
        "cycle_id",
        string="Ikasgaiak"
    )

class EskolaClass(models.Model):
    _name = "eskola.class"
    _description = "Eskola Gelak"

    name = fields.Char(string="Izena", required=True)
    student_number = fields.Integer(string="Ikasle Kopurua", compute='_compute_student_number', store=True)
    students_ids = fields.One2many(
        "eskola.ikasleak",
        "class_id",
        string="Ikasleak"
    )
    cycle_id = fields.Many2one("eskola.cycle", string="Zikloa", required=True, help="Gelaren zikloa")
    location_id = fields.Many2one("stock.location", string="Kokapena", help="Warehouse location assigned to this class")
    equipment_ids = fields.One2many(
        "eskola.equipment",
        "class_id",
        string="Esleitutako Ekipoa",
        help="Ikasleari esleitutako ekipoa"
    ) 

    _sql_constraints = [
        ('unique_location_id', 'UNIQUE(location_id)', 'Each class must have a unique warehouse location'),
    ]
    
    @api.depends('students_ids')
    def _compute_student_number(self):
        for record in self:
            record.student_number = len(record.students_ids)

class EskolaTeacher(models.Model):
    _name = "eskola.teacher"
    _description = "Irakasleak"
    
    image = fields.Image(string="Argazkia")
    name = fields.Char(string="Izena", required=True)
    surname = fields.Char(string="Abizena", required=True)
    user_id = fields.Many2one('res.users', string="User")

class EskolaEquipment(models.Model):
    _name = "eskola.equipment"
    _description = "Eskola Ekipoa"
    
    name = fields.Char(string="Izena", required=True)
    product_id = fields.Many2one("product.product", string="Produktua", required=True, help="Product associated with this equipment")
    equipment_type = fields.Selection([
        ('pc', 'PC'),
        ('screen', 'Screen'),
    ], string="Mota", required=True)
    class_id = fields.Many2one("eskola.class", string="Gela", required=True, help="Equipment location (class/warehouse location)")
    student_id = fields.Many2one("eskola.ikasleak", string="Ikaslea", help="Student assigned to this equipment")
    notes = fields.Text(string="Oharrak")
    incident_ids = fields.One2many(
        "eskola.incident",
        "equipment_id",
        string="Inzidentziak"
    )


class EskolaAttendance(models.Model):
    _name = "eskola.attendance"
    _description = "Ikasleen Faltak"

    date = fields.Date(string="Data", required=True)
    student_id = fields.Many2one("eskola.ikasleak", string="Ikaslea", required=True)
    motive = fields.Selection([
        ("justifikatua", "Justifikatua"),
        ("justifikatu_gabea", "Justifikatu gabea"),
    ], string="Motiboa", required=True)
    note = fields.Char(string="Oharra")

    _sql_constraints = [
        (
            'data_ikasle_unique',
            'unique(date, student_id)',
            'Ikasle honek dagoeneko falta bat du zehaztutako datan.'
        )
    ]


class EskolaSubject(models.Model):
    _name = "eskola.subject"
    _description = "Ikasgaiak"

    name = fields.Char(string="Izena", required=True)
    cycle_id = fields.Many2one("eskola.cycle", string="Zikloa", required=True)


class EskolaGrade(models.Model):
    _name = "eskola.grade"
    _description = "Ikasleen Notak"

    student_id = fields.Many2one("eskola.ikasleak", string="Ikaslea", required=True)
    cycle_id = fields.Many2one("eskola.cycle", string="Zikloa", related="student_id.cycle_id", store=True, readonly=True)
    subject_id = fields.Many2one("eskola.subject", string="Ikasgaia", required=True, domain="[('cycle_id','=',cycle_id)]")
    mark = fields.Float(string="Nota", required=True, help="0-10 arteko nota")

    _sql_constraints = [
        (
            'nota_ikasle_unique',
            'unique(student_id, subject_id)',
            'Ikasle honek dagoeneko nota bat du ikasgai honetarako.'
        )
    ]


class EskolaIncident(models.Model):
    _name = "eskola.incident"
    _description = "Ekipoen Inzidentziak"

    equipment_id = fields.Many2one("eskola.equipment", string="Ekipoa", required=True)
    note = fields.Text(string="Oharra", required=True)
    status = fields.Selection([
        ("pending", "Zain"),
        ("done", "Eginda"),
    ], string="Egoera", required=True, default="pending")