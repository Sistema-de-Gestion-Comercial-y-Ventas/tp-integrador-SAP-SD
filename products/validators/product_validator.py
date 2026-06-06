class ProductValidator:     
    """Validador de datos para productos.Verifica que los datos de entrada cumplen las reglas de negocio."""       
    
    def validate_name(self, name):         
        """Valida que el nombre del producto sea válido. Lanza ValueError si la validación falla."""         
        if not name or len(name.strip()) < 3:             
            raise ValueError('El nombre del producto debe tener al menos 3 caracteres.')       
    
    def validate_price(self, price):         
        """Valida que el precio sea un número positivo."""         
        if not isinstance(price, (int, float)) or price <= 0:             
            raise ValueError('El precio debe ser un número mayor a cero.') 