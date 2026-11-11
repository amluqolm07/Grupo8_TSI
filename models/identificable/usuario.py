
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

import os
import hashlib
import base64

class Usuario(models.Model):
    _name = 'rrhh_upo.usuario'
    _description = 'Usuario identificable en la jerarquía de la UPO.'
    _sql_constraints = [('persona_unique', 'UNIQUE(o2oPersona)', 'Ya tienes un usuario asignado.'),
                        ('username_unique', 'UNIQUE(sUsername)', 'El nombre de usuario ya existe, contacte con un administrador.')]
    _rec_name = 'sEmailCorporativo'
    
    persona_id = fields.Many2one('rrhh_upo.persona', string='Persona', required=True, index=True)
    rol_ids = fields.Many2many('rrhh_upo.rol', string='Roles Asignados', relation='rrhh_upo_usuario_rol_rel')
    
    sUsername = fields.Char(string='Nombre de Usuario', compute='_compute_username', required=True, readonly=True, store=True)
    sEmailCorporativo = fields.Char(string='Correo Electrónico de la UPO', compute='_compute_email_corporativo', required=True, readonly=True, store=True, index=True)
    sPwdEntrada = fields.Char(string='Contraseña', required=True, store=False)
    sPwdHash = fields.Char(string='Hash', required=True, readonly=True)
    sPwdSalt = fields.Char(string='Salt', required=True, readonly=True)
    imFotoPerfil = fields.Image(string='Foto de Perfil', help='Máx. 2MB', max_width=1024, max_height=1024)
    active = fields.Boolean(string='Cuenta Activa', default=True, required=True, readonly=True)
    
    
    def action_bloquear(self):
        
        for record in self:
            if record.active:
                record.active = False
                
            else:
                raise UserError('El usuario ya se encuentra bloqueado.')
    
    
    def action_desbloquear(self):
        
        for record in self:
            if not record.active:
                record.active = True
                
            else:
                raise UserError('El usuario ya se encuentra activo.')
    
    
    def action_validar_pwd(self, pwd):
        
        self.ensure_one()
        
        if self.sPwdHash and self.sPwdSalt and self.active:
            salt = bytes.fromhex(self.sPwdSalt)
            key_pwd = hashlib.pbkdf2_hmac('sha-256', pwd.encode('utf-8'), salt, 100000)
            
            return key_pwd.hex() == self.sPwdHash
        
        return False    
    
    
    def _limpiar_texto(self, texto):
        reemplazos = (('á', 'a'),
                      ('é', 'e'),
                      ('í', 'i'),
                      ('ó', 'o'),
                      ('ú', 'u'),
                      ('ñ', 'n'))
        texto.strip().lower()
        
        for sucio, limpio in reemplazos:
            texto = texto.replace(sucio, limpio)
            
        return texto
    
    
    @api.depends('persona_id.sNombre', 'persona_id.sPrimerApellido', 'persona_id.sSegundoApellido')
    def _compute_username(self):
        
        for record in self:
            persona = record.persona_id
            
            if persona and persona.sNombre and persona.sPrimerApellido:
                nombre = self._limpiar_texto(persona.sNombre)
                primer_apellido = self._limpiar_texto(persona.sPrimerApellido)
                basename = nombre[:3]
                
                if persona.sSegundoApellido:
                    segundo_apellido = self._limpiar_texto(persona.sSegundoApellido)
                    basename += primer_apellido[:3] + segundo_apellido[:3]
                    
                else:
                    basename += primer_apellido
                
                found = False
                contador = 1
                candidato = basename
                dominio = [('sUsername', '=', candidato)]
                dominio.append(('id', '!=', record.id))
                
                while not found:
                    if self.search_count(dominio) == 0:
                        found = True
                    
                    else:
                        candidato = f"{basename}{contador}"
                        contador += 1

                record.sUsername = candidato
    
    
    @api.depends('sUsername')
    def _compute_email_corporativo(self):
        dominio = '@upo.es'
        
        for record in self:
            if record.sUsername:
                record.sEmailCorporativo = f"{record.sUsername}{dominio}"
    
    
    @api.constrains('sPwdEntrada')
    def _check_encrypt_pwd(self):
        
        for record in self:
            if record.sPwdEntrada:
                salt = os.urandom(16)
                key = hashlib.pbkdf2_hmac('sha256', record.sPwdEntrada.encode('utf-8'), salt, 100000)
                
                record.sPwdHash = key.hex()
                record.sPwdSalt = key.hex()
                record.sPwdEntrada = ''
                
                
    @api.constrains('imFotoPerfil')
    def _check_foto_perfil(self):
        max = 2 * 1024 * 1024
        
        for record in self:
            if record.imFotoPerfil:
                tam = len(base64.b64decode(record.imFotoPerfil))
                
                if tam > max:
                    raise ValidationError('El tamaño de la imagen no puede superar los 2MB.')
                