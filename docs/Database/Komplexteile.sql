CREATE TABLE [dbo].[Komplexteile](
	[KomplexteileID] [int] IDENTITY(1,1) NOT NULL,
	[Beschreibung] [nvarchar](50) NULL,
	[WohnungID] [int] NULL,
	[HausID] [int] NULL,
 CONSTRAINT [PK_Komplexteile] PRIMARY KEY CLUSTERED 
(
	[KomplexteileID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Komplexteile]  WITH CHECK ADD  CONSTRAINT [FK_Komplexteile_Haus] FOREIGN KEY([HausID])
REFERENCES [dbo].[Haus] ([HausID])

GO

ALTER TABLE [dbo].[Komplexteile]  WITH CHECK ADD  CONSTRAINT [FK_Komplexteile_Wohnung] FOREIGN KEY([WohnungID])
REFERENCES [dbo].[Wohnung] ([WohnungID])
GO
