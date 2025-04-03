CREATE TABLE [dbo].[Kostensplit](
	[KostensplitID] [int] IDENTITY(1,1) NOT NULL,
	[KostenStelleID] [int] NOT NULL,
	[KomplexID] [int] NULL,
	[HausID] [int] NULL,
	[WohnungID] [int] NULL,
	[Anteil] [decimal](5, 2) NULL,
    CONSTRAINT [PK_Kostensplit] PRIMARY KEY CLUSTERED
(
    [KostensplitID] ASC
)
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Kostensplit]  WITH CHECK ADD  CONSTRAINT [FK_Kostensplit_Haus] FOREIGN KEY([HausID])
REFERENCES [dbo].[Haus] ([HausID])
GO

ALTER TABLE [dbo].[Kostensplit]  WITH CHECK ADD  CONSTRAINT [FK_Kostensplit_Komplex] FOREIGN KEY([KomplexID])
REFERENCES [dbo].[Komplex] ([KomplexID])
GO

ALTER TABLE [dbo].[Kostensplit]  WITH CHECK ADD  CONSTRAINT [FK_Kostensplit_Wohnung] FOREIGN KEY([WohnungID])
REFERENCES [dbo].[Wohnung] ([WohnungID])
GO

ALTER TABLE [dbo].[Kostensplit]  WITH CHECK ADD  CONSTRAINT [FK_Kostensplit_Kostenstelle] FOREIGN KEY([KostenStelleID])
REFERENCES [dbo].[Kostenstelle] ([KostenStelleID])
GO

